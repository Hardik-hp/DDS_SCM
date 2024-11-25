from db_connection import mongo_connect

def create_mongo_database():
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
        # Create a new database (automatically created when data is added)
        admin_db = client.admin
        db_name = "scm"

        # # Enable sharding for the database
        enable_sharding_result = admin_db.command("enableSharding", db_name)
        print(f"Sharding enabled for database '{db_name}': {enable_sharding_result}")

    except Exception as e:
        print("An error occurred while creating the database or inserting data:", e)

    finally:
        # Close the MongoDB connection
        client.close()
        print("Connection to MongoDB closed.")

if __name__ == "__main__":
    create_mongo_database()
