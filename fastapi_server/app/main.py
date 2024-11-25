from fastapi import FastAPI
import psycopg2
from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
from bson import json_util
from fastapi.responses import JSONResponse
import json
# import db_connect as db


# db.connect_to_db("scm")

app = FastAPI()

def get_cockroach_db_connection(db_name):
    """
    Connets to Coakcroach DB and returns connection
    """
    return psycopg2.connect(
        database=db_name,
        user="dds_user",
        password="admin",
        host="host.docker.internal",
        port=26257
    )

def get_mongo_db_connection():
    """
    Connect to the MongoDB mongos router and return the client object.
    """
    try:
        client = MongoClient("mongodb://host.docker.internal:27017/", serverSelectionTimeoutMS=5000)
        return client
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        return None
    except ConfigurationError as e:
        print("Configuration error:", e)
        return None

# ADD APIS as Needed a post and get api have been created.
@app.get("/customers")
async def get_orders():
    conn = get_cockroach_db_connection("scm")
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer")
        orders = cur.fetchall()
        return {"customers": orders}
    finally:
        cur.close()
        conn.close()

@app.post("/create_orders")
async def get_orders(item: dict):
    conn = get_cockroach_db_connection("scm")
    try:
        print(item)
    finally:
        conn.close()
        # cur.close()
        # conn.close()

# Sample Monogo API
@app.get("/orders")
async def get_orders():
    client = get_mongo_db_connection()
    try:
        db = client['scm']
        orders_collection = db["orders"]
        all_orders = list(orders_collection.find())
        return JSONResponse(content=json.loads(json_util.dumps(all_orders)))
    finally:
        client.close()
        print("Connection to MongoDB closed.")