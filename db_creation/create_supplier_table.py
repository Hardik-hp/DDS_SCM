from db_connection.db_connect import connect_to_db

def create_supplier_table():
    conn = connect_to_db("scm")
    if conn:
        try:
            cur = conn.cursor()
            # Create a table with data locality (REGIONAL BY ROW) and composite primary key
            cur.execute("""
                CREATE TABLE IF NOT EXISTS supplier (
                    supplier_id UUID DEFAULT gen_random_uuid(),
                    name STRING,
                    email STRING,
                    phone STRING,
                    region STRING NOT NULL,
                    PRIMARY KEY (region, supplier_id)
                ) LOCALITY REGIONAL BY ROW;
            """)
            conn.commit()
            print("Supplier table with regional locality and composite primary key created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()
