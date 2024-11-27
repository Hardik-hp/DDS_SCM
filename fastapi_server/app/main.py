import traceback
import uuid
from fastapi import FastAPI, HTTPException, Query
from datetime import datetime, timedelta
import psycopg2
from psycopg2.extras import RealDictCursor
from typing import List, Optional
from pydantic import BaseModel, Field
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from bson import json_util
from fastapi.responses import JSONResponse
from uuid import UUID, uuid4
import json
import random

# import db_connect as db


class OrderCreate(BaseModel):
    retailer_id: UUID = Field(default_factory=uuid4)
    product_id: UUID = Field(default_factory=uuid4)
    quantity: float

class ShipmentUpdate(BaseModel):
    shipment_ids: List[str]
    status: str

# Pydantic model for request validation
class ProductCreate(BaseModel):
    name: str = Field(..., max_length=255)
    description: Optional[str] = Field(None, max_length=500)
    price: float = Field(..., ge=0.0)
    region: str = Field(..., max_length=50)

# db.connect_to_db("scm")

app = FastAPI(
    title="Supply Chain Management API",
    description="Scalable API collection for managing orders, shipments, and more.",
    version="1.0.0",
)


def get_cockroach_db_connection(db_name):
    """
    Connets to Coakcroach DB and returns connection
    """
    connection = psycopg2.connect(
            f"postgresql://dds_user:admin@host.docker.internal:26257,host.docker.internal:26258,host.docker.internal:26259/{db_name}?sslmode=require"
        )
    return connection

def get_mongo_db_connection():
    """
    Connect to the MongoDB mongos router and return the client object.
    """
    try:
        client = MongoClient(
            "mongodb://host.docker.internal:27017,host.docker.internal:37017/",
            serverSelectionTimeoutMS=5000,
            replicaSet=None,  # Since mongos doesn't use replica sets, keep this None
        )
        return client
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        return None
    except ConfigurationError as e:
        print("Configuration error:", e)
        return None

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.post("/api/products")
async def create_product(product: ProductCreate):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor()
        # Generate a unique product_id
        product_id = uuid4()
        # SQL query to insert a new product
        cur.execute(
            """
            INSERT INTO products (product_id, name, description, price, region)
            VALUES (%s, %s, %s, %s, %s)
            RETURNING product_id, name, description, price, region
            """,
            (
                str(product_id),  # Convert UUID to string
                product.name,
                product.description,
                product.price,
                product.region,
            ),
        )

        # Fetch the created product details
        created_product = cur.fetchone()
        conn.commit()

        return {
            "message": "Product created successfully",
            "product": created_product,
        }
    except Exception as e:
        conn.rollback()
        raise HTTPException(
            status_code=500,
            detail=f"Failed to create product: {str(e)}"
        )
    finally:
        cur.close()
        conn.close()

@app.get("/api/products/search")
async def search_products(name: str = Query(..., min_length=1, description="Name or part of the product name to search")):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor()

        # Use a SQL query with a LIKE clause for partial matching
        search_query = f"%{name}%"  # Add wildcards for partial match
        cur.execute(
            """
            SELECT product_id, name, description, price, region
            FROM products
            WHERE name ILIKE %s
            """,
            (search_query,),
        )

        # Fetch all matching products
        products = cur.fetchall()
        if not products:
            raise HTTPException(status_code=404, detail="No products found matching the search criteria")

        return {"message": "Products found", "products": products}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to search products: {str(e)}")
    finally:
        cur.close()
        conn.close()

# Sample Monogo API
@app.get("/orders")
async def get_orders():
    client = get_mongo_db_connection()
    try:
        db = client["scm"]
        orders_collection = db["orders"]
        all_orders = list(orders_collection.find())
        return JSONResponse(content=json.loads(json_util.dumps(all_orders)))
    finally:
        client.close()
        print("Connection to MongoDB closed.")

# Get Order by Order ID
@app.get("/orders/{order_id}")
async def get_order_by_id(order_id: str):
    client = get_mongo_db_connection()
    try:
        db = client["scm"]
        orders_collection = db["orders"]
        
        # Find the order by order_id
        order = orders_collection.find_one({"order_id": order_id})
        
        if not order:
            raise HTTPException(status_code=404, detail="Order not found")
        
        return JSONResponse(content=json.loads(json_util.dumps(order)))
    finally:
        client.close()
        print("Connection to MongoDB closed.")

# 1. Shipment Management APIs
@app.get("/api/shipments/outstanding")
async def get_outstanding_deliveries():
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(
            """
            SELECT s.*, o.retailer_id, o.product_id 
            FROM shipments s
            JOIN orders o ON s.order_id = o.order_id
            WHERE s.status != 'Delivered'
        """
        )
        shipments = cur.fetchall()
        return {"shipments": shipments}
    finally:
        cur.close()
        conn.close()


@app.put("/api/shipments/update-status")
async def update_shipment_status(update: ShipmentUpdate):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor()
        # Update shipments
        cur.execute(
            """
            UPDATE shipments 
            SET status = %s, delivery_date = %s 
            WHERE shipment_id = ANY(%s)
            RETURNING order_id
        """,
            (update.status, datetime.now(), update.shipment_ids),
        )

        order_ids = [row[0] for row in cur.fetchall()]

        # Update related orders
        if order_ids:
            cur.execute(
                """
                UPDATE orders 
                SET status = %s 
                WHERE order_id = ANY(%s)
            """,
                (update.status, order_ids),
            )

        conn.commit()
        return {"message": "Successfully updated shipments and orders"}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


@app.post("/api/shipments/create")
async def create_shipment(order_id: int, region: str):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        # Generate fake tracking data
        carriers = ["DHL", "FedEx", "UPS"]
        tracking_number = f"TRACK-{random.randint(10000, 99999)}"
        delivery_date = datetime.now() + timedelta(days=random.randint(3, 7))

        cur.execute(
            """
            INSERT INTO shipments (carrier, tracking_number, status, shipment_date, delivery_date, order_id, region)
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING *
        """,
            (
                random.choice(carriers),
                tracking_number,
                "Pending",
                datetime.now(),
                delivery_date,
                str(order_id),
                region,
            ),
        )

        shipment = cur.fetchone()
        conn.commit()
        return shipment
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()


# 2. Order Creation with Inventory Check
@app.post("/api/orders")
async def create_order(order: OrderCreate):
    conn = get_cockroach_db_connection("scm")
    client = get_mongo_db_connection()
        
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)

        # Check inventory
        cur.execute(
            """
            SELECT warehouse_id, quantity 
            FROM warehouses
            WHERE product_id = %s AND quantity >= %s 
            LIMIT 1
        """,
            (str(order.product_id), order.quantity),
        )

        warehouse_info = cur.fetchone()
        if not warehouse_info:
            raise HTTPException(status_code=400, detail="Insufficient inventory")

        # Check retailer
        cur.execute(
            """
            SELECT * 
            from retailers
            WHERE retailer_id = %s
        """,
            (str(order.retailer_id),)
        )
        retailer = cur.fetchone()
        if not retailer:
            raise HTTPException(status_code=400, detail="Unregistered Retailer")

        # Create order
        db = client["scm"]
        orders_collection = db["orders"]
        order_id = str(uuid.uuid4())
        order_document = {
            "order_id": order_id,
            "retailer_id": str(order.retailer_id),
            "product_id": str(order.product_id),
            "order_date": datetime.now(),
            "status": "Pending",
            "quantity": order.quantity,
            "shipping_address": retailer["address"],
            "region": retailer["region"]
        }
        # Insert the order into MongoDB
        orders_collection.insert_one(order_document)

        # Update inventory
        cur.execute(
            """
            UPDATE warehouses 
            SET quantity = quantity - %s 
            WHERE warehouse_id = %s AND product_id = %s
        """,
            (order.quantity, str(warehouse_info["warehouse_id"]), str(order.product_id)),
        )

        # Create shipment
        shipment = await create_shipment(order_id, retailer["region"])

        conn.commit()
        return {"order_id": order_id, "shipment": shipment}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

@app.get("/api/{resource}")
async def get_resource(resource: str):
    valid_resources = {"retailers", "products", "suppliers", "shipments", "warehouses"}
    if resource not in valid_resources:
        raise HTTPException(status_code=400, detail="Invalid resource type")

    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {resource}")
        return cur.fetchall()
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()

# 3. CRUD Operations for Customers/Products/Suppliers
@app.get("/api/{resource}/{id}")
async def get_resource(resource: str, id: UUID):
    valid_resources = {"retailers", "products", "suppliers", "shipments", "warehouses"}
    if resource not in valid_resources:
        raise HTTPException(status_code=400, detail="Invalid resource type")

    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute(f"SELECT * FROM {resource} WHERE {resource[:-1]}_id = %s", (str(id),))
        result = cur.fetchone()
        if not result:
            raise HTTPException(status_code=404, detail=f"{resource[:-1]} not found")
        return result
    finally:
        cur.close()
        conn.close()


# 4. Warehouse Operations
@app.get("/api/warehouse/inventory/{product_id}")
async def get_warehouse_inventory(
    product_id: str, min_quantity: Optional[float] = None
):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        query = "SELECT * FROM warehouse WHERE product_id = %s"
        params = [product_id]

        if min_quantity is not None:
            query += " AND quantity >= %s"
            params.append(min_quantity)

        cur.execute(query, params)
        inventory = cur.fetchall()
        return {"inventory": inventory}
    finally:
        cur.close()
        conn.close()


@app.put("/api/warehouse/inventory")
async def update_inventory(warehouse_id: int, product_id: int, quantity_change: float):
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE warehouse 
            SET quantity = quantity + %s 
            WHERE warehouse_id = %s AND product_id = %s
            RETURNING quantity
        """,
            (quantity_change, warehouse_id, product_id),
        )

        result = cur.fetchone()
        if not result:
            raise HTTPException(
                status_code=404, detail="Warehouse inventory record not found"
            )

        conn.commit()
        return {"new_quantity": result[0]}
    except Exception as e:
        conn.rollback()
        raise HTTPException(status_code=500, detail=str(e))
    finally:
        cur.close()
        conn.close()
