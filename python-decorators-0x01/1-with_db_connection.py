import sqlite3
import functools
import os

DB_FILE = "users.db"

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

def with_db_connection(func):
    """
    Decorator that opens a database connection, passes it to the function,
    and closes it afterwards.
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
        try:
            # Pass the connection as the first argument
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
            # print("Database connection closed.") # Optional: for verification
    return wrapper

@with_db_connection
def get_user_by_id(conn, user_id):
    """Fetches a user by their ID from the database."""
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = ?", (user_id,))
    return cursor.fetchone()

#### Fetch user by ID with automatic connection handling
if __name__ == "__main__":
    setup_database()
    user = get_user_by_id(user_id=1)
    print(f"Fetched user: {user}")
    
    user2 = get_user_by_id(user_id=2)
    print(f"Fetched user: {user2}")

    # Clean up the database file after execution
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
