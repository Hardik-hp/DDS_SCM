from db_load_data.load_customer_data import load_customer_data
from db_load_data.load_warehouse_data import load_warehouse_data
from db_load_data.load_product_data import load_product_data
from db_load_data.load_supplier_data import load_supplier_data
from db_load_data.load_shipments_data import load_shipments_data
from db_connection.db_connect import connect_to_db

def truncate_data(conn, relation):
    try:
        cur = conn.cursor()
        cur.execute(f"TRUNCATE TABLE {relation}")
        conn.commit()
        print(f"{relation} data truncated successfully.")
    except Exception as e:
        print(f"Error removing data: {e} for table {relation}")

def load_data():
    conn = connect_to_db("scm")
    if conn:
        tables = ['products', 'supplier', 'customer', 'warehouse', 'shipments']
        for table in tables: truncate_data(conn, table)

        customer_data_file_path = "./data_files/customer_data.csv"
        warehouse_data_file_path = "./data_files/warehouse_data.csv"
        products_data_file_path = "./data_files/products_data.csv"
        supplier_data_file_path = "./data_files/supplier_data.csv"
        shipments_data_file_path = "./data_files/shipments_data.csv"
        load_customer_data(conn, customer_data_file_path)
        load_warehouse_data(conn, warehouse_data_file_path)
        load_product_data(conn, products_data_file_path)
        load_supplier_data(conn, supplier_data_file_path)
        load_shipments_data(conn, shipments_data_file_path)
    conn.close()

if __name__ == "__main__":
    load_data()  # Initializes the database and creates the tables
