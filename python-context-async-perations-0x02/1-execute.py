import sqlite3
import os

DB_FILE = "users.db"

class ExecuteQuery:
    """A reusable context manager for executing a given SQL query."""
    def __init__(self, db_file, query, params=()):
        self.db_file = db_file
        self.query = query
        self.params = params
        self.conn = None

    def __enter__(self):
        """Connects to the DB, executes the query, and returns the cursor."""
        print("Connecting to the database...")
        self.conn = sqlite3.connect(self.db_file)
        self.conn.row_factory = sqlite3.Row
        cursor = self.conn.cursor()
        print(f"Executing query: {self.query} with params {self.params}")
        cursor.execute(self.query, self.params)
        return cursor

    def __exit__(self, exc_type, exc_val, exc_tb):
        """Commits the transaction and closes the connection."""
        if self.conn:
            if exc_type is None:
                # No exception, commit the transaction
                self.conn.commit()
                print("Transaction committed.")
            else:
                # An exception occurred, rollback is implicit with connection close
                print(f"An exception occurred: {exc_val}. Rolling back.")
            self.conn.close()
            print("Database connection closed.")
        # Return False to propagate any exceptions
        return False

def setup_database():
    """Sets up the database with a users table including age."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    conn = sqlite3.connect(DB_FILE)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER
    )
    """
    )
    users_to_add = [
        (1, "Alice", "alice@example.com", 30),
        (2, "Bob", "bob@example.com", 22),
        (3, "Charlie", "charlie@example.com", 28),
        (4, "David", "david@example.com", 25)
    ]
    cursor.executemany("INSERT INTO users (id, name, email, age) VALUES (?, ?, ?, ?)", users_to_add)
    conn.commit()
    conn.close()

if __name__ == "__main__":
    setup_database()

    print("--- Using the ExecuteQuery context manager ---")
    query = "SELECT * FROM users WHERE age > ?"
    params = (25,)

    try:
        with ExecuteQuery(DB_FILE, query, params) as cursor:
            results = cursor.fetchall()
            
            print("\nQuery results (users older than 25):")
            if results:
                for row in results:
                    print(dict(row))
            else:
                print("No users found matching the criteria.")

    except Exception as e:
        print(f"\nAn error occurred outside the context manager: {e}")

    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
