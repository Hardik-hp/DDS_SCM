from datetime import datetime
from random import choice
from db_connection import mongo_connect
import json


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

        if "orders" in db.list_collection_names():
            db["orders"].drop()
            print("Existing 'orders' collection dropped.")
        
        orders_collection = db["orders"]
        # Sample data to insert
        with open("./orders_data.json", "r") as file:
            sample_orders = json.load(file)
            # Insert the sample data into the collection
            orders_collection.insert_many(sample_orders)

            print("Orders collection created successfully with sample records!")
    except Exception as e:
        print("An error occurred while creating the database or inserting data:", e)

    finally:
        # Close the MongoDB connection
        client.close()
        print("Connection to MongoDB closed.")


if __name__ == "__main__":
    create_orders_collection()
