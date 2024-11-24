from pymongo import MongoClient
from pymongo.errors import ConnectionFailure, ConfigurationError
# MONGO_URI = "mongodb://localhost:27017/"

def connect_to_mongo():
    """
    Connect to the MongoDB mongos router and return the client object.
    """
    try:
        client = MongoClient("mongodb://localhost:27017/", serverSelectionTimeoutMS=5000)
        # Ping the server to verify the connection
        # client.admin.command("ping")
        # print("Connected to the MongoDB mongos router successfully.")
        return client
    except ConnectionFailure as e:
        print("Failed to connect to MongoDB:", e)
        return None
    except ConfigurationError as e:
        print("Configuration error:", e)
        return None