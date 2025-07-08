import time
import sqlite3
import functools
import os

DB_FILE = "users.db"

# --- Database Setup ---
def setup_database():
    """Initializes the database with a users table and sample data."""
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

# --- Decorators ---
def with_db_connection(func):
    """Decorator to handle database connection automatically."""
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        conn = sqlite3.connect(DB_FILE)
        try:
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def retry_on_failure(retries=3, delay=2):
    """
    Decorator factory that retries a function if it raises an exception.
    """
    def decorator(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(1, retries + 1):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    print(f"Attempt {attempt} failed: {e}. Retrying in {delay} seconds...")
                    if attempt == retries:
                        print("All retries failed.")
                        raise
                    time.sleep(delay)
        return wrapper
    return decorator

# --- Test Functions ---

# To simulate failure, we'll use a global counter.
# The function will fail for the first two attempts.
ATTEMPT_COUNTER = 0

@with_db_connection
@retry_on_failure(retries=3, delay=1)
def fetch_users_with_retry(conn):
    """Fetches users, simulating failure on the first two attempts."""
    global ATTEMPT_COUNTER
    ATTEMPT_COUNTER += 1
    
    print(f"Executing fetch_users_with_retry, attempt number {ATTEMPT_COUNTER}")
    
    if ATTEMPT_COUNTER <= 2:
        # Simulate a transient error
        raise sqlite3.OperationalError("Database is locked, please try again.")
    
    # On the third attempt, it should succeed
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users")
    print("Query executed successfully.")
    return cursor.fetchall()

# --- Main Execution ---
if __name__ == "__main__":
    setup_database()
    
    print("--- Attempting to fetch users with retry logic ---")
    try:
        users = fetch_users_with_retry()
        print("\nSuccessfully fetched users:")
        for user in users:
            print(user)
    except Exception as e:
        print(f"\nCaught an exception after all retries: {e}")

    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
