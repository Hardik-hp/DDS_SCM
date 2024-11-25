from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
from pymongo import MongoClient
from pymongo import MongoClient


# db.connect_to_db("scm")

app = FastAPI()

def get_db_connection():
    return psycopg2.connect(
        database="scm",
        user="dds_user",
        password="admin",
        host="host.docker.internal",
        port=26257
    )

def get_mongo_connection():
    client = MongoClient("mongodb://host.docker.internal:27017/", serverSelectionTimeoutMS=5000)
    return client

def get_mongo_connection():
    client = MongoClient("mongodb://host.docker.internal:27017/", serverSelectionTimeoutMS=5000)
    return client

# ADD APIS as Needed a post and get api have been created.
@app.get("/customers")
async def get_customers():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer")
        customers = cur.fetchall()
        return {"customers": customers}
    finally:
        cur.close()
        conn.close()

@app.post("/create_orders")
async def get_orders(item: dict):
    conn = get_db_connection()
    try:
        print(item)
    finally:
        conn.close()
        # cur.close()
        # conn.close()

@app.post("/orders")
async def get_orders():
    client = get_mongo_connection()
    db = client["scm"]
    orders_collection = db["orders"]
    # Fetch orders from MongoDB
    mongo_orders = list(orders_collection.find({}, {"_id": 0}))
    response = {
        "mongo_orders": mongo_orders
    }
    return response

@app.post("/orders")
async def get_orders():
    client = get_mongo_connection()
    db = client["scm"]
    orders_collection = db["orders"]
    # Fetch orders from MongoDB
    mongo_orders = list(orders_collection.find({}, {"_id": 0}))
    response = {
        "mongo_orders": mongo_orders
    }
    return response
