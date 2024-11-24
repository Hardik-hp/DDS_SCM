from db_load_data.load_customer_data import load_customer_data
from db_load_data.load_warehouse_data import load_warehouse_data
from db_connection.db_connect import connect_to_db

def load_data():
    conn = connect_to_db("scm")
    if conn:
        customer_data_file_path = "./data_files/customer_data.csv"
        warehouse_data_file_path = "./data_files/warehouse_data.csv"
        load_customer_data(conn, customer_data_file_path)
        load_warehouse_data(conn, warehouse_data_file_path)

if __name__ == "__main__":
    load_data()  # Initializes the database and creates the tables
