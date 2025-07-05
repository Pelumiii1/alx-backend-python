#!/usr/bin/python3
"""
This module contains functions for lazy pagination of user data.
"""
seed = __import__('seed')

def paginate_users(page_size, offset):
    """Fetches a page of users from the database."""
    connection = seed.connect_to_prodev()
    if not connection:
        return []
    
    rows = []
    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute(f"SELECT * FROM user_data LIMIT {page_size} OFFSET {offset}")
        rows = cursor.fetchall()
    except Exception as e:
        print(f"An error occurred: {e}")
    finally:
        if connection.is_connected():
            connection.close()
    return rows

def lazy_pagination(page_size):
    """
    Lazily fetches paginated data from the users database
    using a generator.
    """
    offset = 0
    while True:
        page = paginate_users(page_size, offset)
        if not page:
            break
        yield page
        offset += page_size
