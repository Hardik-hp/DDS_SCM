import csv
import os
from db_connection.db_connect import connect_to_db

# Function to load data into the customer table
def load_product_data(conn, csv_file_path):
    try:
        cur = conn.cursor()
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute("""
                    INSERT INTO products (product_id, name, description, price, region)
                    VALUES (%s, %s, %s, %s, %s);
                """, (row["product_id"], row["name"], row["description"], float(row["price"]), row["region"]))
        conn.commit()
        print("Products data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

# Main execution
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "products_data.csv")

    conn = connect_to_db("scm")
    if conn:
        load_product_data(conn, csv_file_path)
