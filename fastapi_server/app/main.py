from fastapi import FastAPI
import psycopg2
from psycopg2.extras import RealDictCursor
# import db_connect as db


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

# ADD APIS as Needed a post and get api have been created.
@app.get("/orders")
async def get_orders():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM customer")
        orders = cur.fetchall()
        return {"orders": orders}
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
