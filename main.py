from db_creation.init_db import initialize_database

if __name__ == "__main__":
    print("Initializing the database and creating tables...")
    initialize_database()  # Initializes the database and creates the tables
    print("Database and tables are set up successfully.")
