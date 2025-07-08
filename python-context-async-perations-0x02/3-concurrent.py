import asyncio
import aiosqlite
import os

DB_FILE = "users_async.db"

async def setup_database():
    """Sets up the database with a users table and sample data."""
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
    async with aiosqlite.connect(DB_FILE) as db:
        await db.execute("""
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            name TEXT NOT NULL,
            age INTEGER
        )
        """)
        users_to_add = [
            ("Alice", 30),
            ("Bob", 45),
            ("Charlie", 28),
            ("David", 50)
        ]
        await db.executemany("INSERT INTO users (name, age) VALUES (?, ?)", users_to_add)
        await db.commit()

async def async_fetch_users():
    """Fetches all users from the database asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users") as cursor:
            results = await cursor.fetchall()
            print("Fetched all users.")
            return [dict(row) for row in results]

async def async_fetch_older_users():
    """Fetches users older than 40 from the database asynchronously."""
    async with aiosqlite.connect(DB_FILE) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
            results = await cursor.fetchall()
            print("Fetched users older than 40.")
            return [dict(row) for row in results]

async def fetch_concurrently():
    """Runs both fetch queries concurrently and prints the results."""
    # Setup the database before running queries
    await setup_database()
    
    # Run the two fetch functions concurrently
    all_users, older_users = await asyncio.gather(
        async_fetch_users(),
        async_fetch_older_users()
    )
    
    print("\n--- All Users ---")
    for user in all_users:
        print(user)
        
    print("\n--- Users Older Than 40 ---")
    for user in older_users:
        print(user)

if __name__ == "__main__":
    print("Running database queries concurrently...")
    asyncio.run(fetch_concurrently())
    
    # Clean up the database file
    if os.path.exists(DB_FILE):
        os.remove(DB_FILE)
