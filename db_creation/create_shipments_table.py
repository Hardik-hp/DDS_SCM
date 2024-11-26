from db_connection.db_connect import connect_to_db

def create_shipments_table():
    conn = connect_to_db("scm")
    if conn:
        try:
            cur = conn.cursor()
            # Create a table with data locality (REGIONAL BY ROW) and composite primary key
            cur.execute("""
                CREATE TABLE IF NOT EXISTS shipments (
                    shipment_id UUID DEFAULT gen_random_uuid(),
                    carrier STRING,
                    tracking_number STRING,
                    status STRING,
                    shipment_date TIMESTAMPTZ DEFAULT current_timestamp,
                    delivery_date TIMESTAMPTZ DEFAULT current_timestamp + INTERVAL '5 days',
                    order_id UUID,
                    region STRING NOT NULL,
                    PRIMARY KEY (region, shipment_id)
                ) LOCALITY REGIONAL BY ROW;
            """)
            conn.commit()
            print("Shipments table with regional locality and composite primary key created successfully.")
        except Exception as e:
            print(f"Error creating table: {e}")
        finally:
            conn.close()
