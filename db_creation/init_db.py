from db_creation.create_database import create_database
from db_creation.create_customer_table import create_customer_table
from db_creation.create_warehouse_table import create_warehouse_table

def initialize_database():
    create_database("scm")
    create_customer_table()  # Create the customer table after the database is created
    create_warehouse_table()
    print("Database and table setup complete.")

if __name__ == "__main__":
    initialize_database()
