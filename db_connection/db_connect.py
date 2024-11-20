import psycopg2

def connect_to_db(db_name):
    try:
        # Define SSL parameters
        ssl_params = {
            "sslmode": "verify-full",
            "sslrootcert": "./certs/ca.crt",  # Path to CA certificate
            "sslcert": "./certs/client.root.crt",  # Path to client certificate
            "sslkey": "./certs/client.root.key"   # Path to client key
        }

        # Now connect to the created database
        conn = psycopg2.connect(
            dbname=db_name,  # Connect to the `db_name` database
            user="root",
            password="",  # Password if required; otherwise, omit
            host="localhost",
            port="26257",
            **ssl_params  # Add SSL parameters
        )
        print(f"Connected to CockroachDB '{db_name}' database securely")
        return conn
    except Exception as e:
        print(f"Error connecting to CockroachDB: {e}")
        return None
