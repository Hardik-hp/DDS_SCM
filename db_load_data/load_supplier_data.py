import csv
import os
from db_connection.db_connect import connect_to_db

# Function to load data into the customer table
def load_supplier_data(conn, csv_file_path):
    try:
        cur = conn.cursor()
        with open(csv_file_path, mode="r") as file:
            reader = csv.DictReader(file)
            for row in reader:
                cur.execute("""
                    INSERT INTO supplier (supplier_id, name, email, phone, region)
                    VALUES (%s, %s, %s, %s, %s);
                """, (row["supplier_id"], row["name"], row["email"], row["phone"], row["region"]))
        conn.commit()
        print("Supplier data loaded successfully.")
    except Exception as e:
        print(f"Error loading data: {e}")
    finally:
        conn.close()

# Main execution
if __name__ == "__main__":
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_file_path = os.path.join(script_dir, "supplier_data.csv")

    conn = connect_to_db("scm")
    if conn:
        load_supplier_data(conn, csv_file_path)
