from datetime import datetime
from random import choice
from db_connection import mongo_connect

def create_orders_collection():
    """
    Create a new database and a collection, and insert sample data.
    Utilizes the MongoDB connection established in mongodb_connection.py.
    """
    # Connect to MongoDB
    client = mongo_connect.connect_to_mongo()
    if not client:
        print("Could not establish connection to MongoDB. Exiting...")
        return

    try:
        db = client["scm"]
        orders_collection = db["orders"]
        # Sample data to insert
        sample_orders = [
            {
                "order_id": 1,
                "customer_id": 101,
                "product_id": 201,
                "order_date": datetime(2024, 11, 1, 14, 30),
                "status": "Pending",
                "quantity": 2,
                "shipping_address": "123 Main St, Springfield, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 2,
                "customer_id": 102,
                "product_id": 202,
                "order_date": datetime(2024, 11, 2, 10, 15),
                "status": "Shipped",
                "quantity": 1,
                "shipping_address": "456 Oak Ave, Chicago, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 3,
                "customer_id": 103,
                "product_id": 203,
                "order_date": datetime(2024, 11, 3, 16, 45),
                "status": "Delivered",
                "quantity": 3,
                "shipping_address": "789 Pine Rd, Peoria, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 4,
                "customer_id": 101,
                "product_id": 204,
                "order_date": datetime(2024, 11, 4, 12, 0),
                "status": "Pending",
                "quantity": 4,
                "shipping_address": "123 Main St, Springfield, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 5,
                "customer_id": 102,
                "product_id": 205,
                "order_date": datetime(2024, 11, 5, 9, 30),
                "status": "Shipped",
                "quantity": 2,
                "shipping_address": "456 Oak Ave, Chicago, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 6,
                "customer_id": 104,
                "product_id": 206,
                "order_date": datetime(2024, 11, 6, 14, 0),
                "status": "Delivered",
                "quantity": 1,
                "shipping_address": "321 Elm St, Naperville, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 7,
                "customer_id": 105,
                "product_id": 207,
                "order_date": datetime(2024, 11, 7, 17, 15),
                "status": "Pending",
                "quantity": 5,
                "shipping_address": "654 Maple Dr, Aurora, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 8,
                "customer_id": 103,
                "product_id": 208,
                "order_date": datetime(2024, 11, 8, 11, 45),
                "status": "Shipped",
                "quantity": 3,
                "shipping_address": "789 Pine Rd, Peoria, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 9,
                "customer_id": 106,
                "product_id": 209,
                "order_date": datetime(2024, 11, 9, 15, 30),
                "status": "Delivered",
                "quantity": 2,
                "shipping_address": "987 Birch Ln, Champaign, IL",
                "region": choice([1, 2, 3])
            },
            {
                "order_id": 10,
                "customer_id": 105,
                "product_id": 210,
                "order_date": datetime(2024, 11, 10, 13, 0),
                "status": "Pending",
                "quantity": 1,
                "shipping_address": "654 Maple Dr, Aurora, IL",
                "region": choice([1, 2, 3])
            },
        ]

        # Insert the sample data into the collection
        orders_collection.insert_many(sample_orders)


        print("Orders collection created successfully with 10 sample records!")
        # create collection

    except Exception as e:
        print("An error occurred while creating the database or inserting data:", e)

    finally:
        # Close the MongoDB connection
        client.close()
        print("Connection to MongoDB closed.")

if __name__ == "__main__":
    create_orders_collection()
