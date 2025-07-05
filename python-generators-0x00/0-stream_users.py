#!/usr/bin/python3
"""
This module contains a generator function to stream users from the database.
"""
import mysql.connector
from seed import connect_to_prodev

def stream_users():
    """Fetches rows one by one from the user_data table."""
    connection = connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            for row in cursor:
                yield row
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()
