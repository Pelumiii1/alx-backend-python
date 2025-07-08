import sqlite3
import os

DB_FILE = "users.db"

class DatabaseConnection:
    """A class-based context manager for handling database connections."""
    def __init__(self, db_file):
        self.db_file = db_file
        self.conn = None

    def __enter__(self):
        """Opens the database connection and returns a cursor."""
        print("Connecting to the database...")
        self.conn = sqlite3.connect(self.db_file)
        # Set row_factory to access columns by name
        self.conn.row_factory = sqlite3.Row
        return self.conn.cursor()

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Closes the database connection."""
        if self.conn:
            self.conn.close()
            print("Database connection closed.")
        # If an exception occurred, this will return False, propagating the exception
        return False

def setup_database():
    """Sets up the database with a users table and some sample data."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL
    )
    """)
    cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (1, "Alice", "alice@example.com"))
    cursor.execute("INSERT INTO users (id, name, email) VALUES (?, ?, ?)", (2, "Bob", "bob@example.com"))
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()

    print("--- Using the context manager to fetch users ---")
    try:
        with DatabaseConnection(DB_FILE) as cursor:
            cursor.execute("SELECT * FROM users")
            results = cursor.fetchall()
            
            print("Query results:")
            for row in results:
                print(dict(row))

    except Exception as e:
        print(f"An error occurred: {e}")

    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
