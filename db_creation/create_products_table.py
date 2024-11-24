from db_connection.db_connect import connect_to_db

def create_products_table():
    conn = connect_to_db("scm")
    if conn:
        try:
            cur = conn.cursor()
            # Create a table with data locality (REGIONAL BY ROW) and composite primary key
            cur.execute("""
                CREATE TABLE IF NOT EXISTS products (
                    product_id UUID DEFAULT gen_random_uuid(),
                    name STRING,
                    description STRING,
                    price DECIMAL,
                    region STRING NOT NULL,
                    PRIMARY KEY (region, product_id)
                ) LOCALITY REGIONAL BY ROW;
            """)
            conn.commit()
            print("Products table with regional locality and composite primary key created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()
