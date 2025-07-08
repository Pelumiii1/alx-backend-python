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
            result = func(conn, *args, **kwargs)
            return result
        finally:
            conn.close()
    return wrapper

def transactional(func):
    """
    Decorator that ensures a function running a database operation is wrapped
    inside a transaction. If the function raises an error, it rolls back;
    otherwise, it commits the transaction.
    """
    @functools.wraps(func)
    def wrapper(conn, *args, **kwargs):
        try:
            result = func(conn, *args, **kwargs)
            conn.commit()
            print("Transaction committed.")
            return result
        except Exception as e:
            conn.rollback()
            print(f"Transaction rolled back due to error: {e}")
            raise
    return wrapper

@with_db_connection
def get_user_email(conn, user_id):
    """A helper to get the current email of a user."""
    cursor = conn.cursor()
    cursor.execute("SELECT email FROM users WHERE id = ?", (user_id,))
    result = cursor.fetchone()
    return result[0] if result else None

@with_db_connection
@transactional
def update_user_email(conn, user_id, new_email):
    """Updates a user's email in a transaction."""
    cursor = conn.cursor()
    print(f"Updating user {user_id} email to {new_email}")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))

@with_db_connection
@transactional
def update_with_error(conn, user_id, new_email):
    """Attempts to update an email but raises an error to test rollback."""
    cursor = conn.cursor()
    print(f"Attempting to update user {user_id} email to {new_email}, but will fail.")
    cursor.execute("UPDATE users SET email = ? WHERE id = ?", (new_email, user_id))
    raise ValueError("Simulating a failure after update")

if __name__ == "__main__":
    setup_database()

    # --- Test Case 1: Successful Transaction ---
    print("--- Running successful transaction test ---")
    user_id = 1
    new_email = "Crawford_Cartwright@hotmail.com"
    print(f"Email for user {user_id} before update: {get_user_email(user_id=user_id)}")
    update_user_email(user_id=user_id, new_email=new_email)
    print(f"Email for user {user_id} after update: {get_user_email(user_id=user_id)}")
    print("")

    # --- Test Case 2: Failed Transaction (Rollback) ---
    print("--- Running failed transaction test ---")
    user_id_fail = 2
    new_email_fail = "fail.test@example.com"
    print(f"Email for user {user_id_fail} before failed update: {get_user_email(user_id=user_id_fail)}")
    try:
        update_with_error(user_id=user_id_fail, new_email=new_email_fail)
    except ValueError as e:
        print(f"Caught expected error: {e}")
    print(f"Email for user {user_id_fail} after failed update: {get_user_email(user_id=user_id_fail)}")
    print("")

    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)