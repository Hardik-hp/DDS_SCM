from db_creation.create_database import create_database
from db_creation.create_customer_table import create_customer_table
from db_creation.create_warehouse_table import create_warehouse_table
from db_creation.create_products_table import create_products_table
from db_creation.create_supplier_table import create_supplier_table
from db_creation.create_mongo_database import create_mongo_database
from db_creation.create_orders_collection import create_orders_collection
from db_creation.create_shipments_table import create_shipments_table

def initialize_database():
    create_database("scm")
    create_customer_table()  # Create the customer table after the database is created
    create_warehouse_table()
    create_products_table()
    create_supplier_table()
    create_shipments_table()
    # create_mongo_database()
    create_orders_collection()
    print("Database, tables and collections setup complete.")

if __name__ == "__main__":
    initialize_database()
