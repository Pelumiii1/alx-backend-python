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
        # The query is passed as a keyword argument or positional argument
        # The decorator itself doesn't need the connection object
        conn = sqlite3.connect(DB_FILE)
        try:
            # Pass the connection as the first argument to the decorated function
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

query_cache = {}

def cache_query(func):
    """
    Decorator that caches the results of a database query based on the SQL query string.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        # Extract the query string from either args or kwargs
        if args:
            query = args[0]
        else:
            query = kwargs.get('query')

        if query in query_cache:
            print(f"Cache hit for query: '{query}'")
            return query_cache[query]
        
        print(f"Cache miss for query: '{query}'. Executing and caching result.")
        result = func(conn, *args, **kwargs)
        query_cache[query] = result
        return result
    return wrapper

# --- Decorated Function ---
@with_db_connection
@cache_query
def fetch_users_with_cache(conn, query):
    """Fetches users from the database. The result will be cached."""
    print("Executing database query...")
    cursor = conn.cursor()
    cursor.execute(query)
    time.sleep(1) # Simulate a delay to show the benefit of caching
    results = cursor.fetchall()
    print("Query finished.")
    return results

# --- Main Execution ---
if __name__ == "__main__":
    setup_database()
    
    print("--- First call (should execute and cache) ---")
    start_time = time.time()
    users1 = fetch_users_with_cache(query="SELECT * FROM users")
    duration1 = time.time() - start_time
    print(f"First call took {duration1:.2f} seconds.")
    print("Users fetched:", users1)
    print("\n")

    print("--- Second call (should hit the cache) ---")
    start_time = time.time()
    users2 = fetch_users_with_cache(query="SELECT * FROM users")
    duration2 = time.time() - start_time
    print(f"Second call took {duration2:.2f} seconds.")
    print("Users fetched again:", users2)
    print("\n")

    print("--- Third call with different query (should execute and cache) ---")
    start_time = time.time()
    user_alice = fetch_users_with_cache(query="SELECT * FROM users WHERE name = 'Alice'")
    duration3 = time.time() - start_time
    print(f"Third call took {duration3:.2f} seconds.")
    print("User Alice fetched:", user_alice)
    print("\n")

    print("--- Fourth call with same different query (should hit cache) ---")
    start_time = time.time()
    user_alice_again = fetch_users_with_cache(query="SELECT * FROM users WHERE name = 'Alice'")
    duration4 = time.time() - start_time
    print(f"Fourth call took {duration4:.2f} seconds.")
    print("User Alice fetched again:", user_alice_again)
    print("\n")

    print("Current cache state:", query_cache)

    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
