from db_connection.db_connect import connect_to_db

def create_warehouse_table():
    conn = connect_to_db("scm")
    if conn:
        try:
            cur = conn.cursor()
            # Create warehouse table with UUID warehouse_id and data locality
            cur.execute("""
                CREATE TABLE IF NOT EXISTS warehouses (
                    warehouse_id UUID DEFAULT gen_random_uuid(),
                    product_id UUID,
                    quantity INT,
                    supplier_id UUID,
                    region STRING NOT NULL,
                    PRIMARY KEY (region, warehouse_id, product_id)
                ) LOCALITY REGIONAL BY ROW;
            """)
            conn.commit()
            print("Warehouse table with UUID, regional locality and composite primary key created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()