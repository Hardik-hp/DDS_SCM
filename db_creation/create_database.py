import psycopg2

def create_database(db_name):
    try:
        # Define SSL parameters
        ssl_params = {
            "sslmode": "verify-full",
            "sslrootcert": "./certs/ca.crt",  # Path to CA certificate
            "sslcert": "./certs/client.root.crt",  # Path to client certificate
            "sslkey": "./certs/client.root.key"   # Path to client key
        }
        # First connect to the `defaultdb` to check/create the required database
        init_conn = psycopg2.connect(
            dbname="defaultdb",  # Connect to the defaultdb database to create/check `db_name`
            user="root",
            password="",  # Password if required; otherwise, omit
            host="localhost",
            port="26257",
            **ssl_params  # Add SSL parameters
        )
        init_conn.autocommit = True  # Enable autocommit for DDL statements
        cur = init_conn.cursor()

        # Check if the database exists; create it if it doesn't
        cur.execute(f"SELECT COUNT(*) FROM [SHOW DATABASES] WHERE database_name = '{db_name}';")
        if cur.fetchone()[0] == 0:
            print(f"Database '{db_name}' does not exist. Creating it...")
            cur.execute(f"CREATE DATABASE {db_name};")
            cur.execute(f"ALTER DATABASE {db_name} SET PRIMARY REGION 'us-east';")
            cur.execute(f"ALTER DATABASE {db_name} ADD REGION 'us-west';")
            cur.execute(f"ALTER DATABASE {db_name} ADD REGION 'us-central';")
            cur.execute("ALTER RANGE default CONFIGURE ZONE USING constraints = '{+region=us-east}';")
            cur.execute("ALTER RANGE default CONFIGURE ZONE USING constraints = '{+region=us-west}';")
            cur.execute("ALTER RANGE default CONFIGURE ZONE USING constraints = '{+region=us-central}';")
            print(f"Database '{db_name}' created successfully.")

        cur.close()
        init_conn.close()
    except Exception as e:
        print(f"Error creating database scm: {e}")
        return None