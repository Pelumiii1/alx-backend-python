#!/usr/bin/python3
"""
This module contains functions for batch processing of user data.
"""
import mysql.connector
from seed import connect_to_prodev

def stream_users_in_batches(batch_size=50):
    """Fetches rows in batches from the user_data table."""
    connection = connect_to_prodev()
    if connection:
        try:
            cursor = connection.cursor(dictionary=True)
            cursor.execute("SELECT * FROM user_data")
            while True:
                batch = cursor.fetchmany(batch_size)
                if not batch:
                    break
                yield batch
        except mysql.connector.Error as err:
            print(f"Error: {err}")
        finally:
            if connection.is_connected():
                cursor.close()
                connection.close()

def batch_processing(batch_size=50):
    """Processes each batch to filter users over the age of 25."""
    user_batches = stream_users_in_batches(batch_size)
    for batch in user_batches:
        for user in batch:
            if user['age'] > 25:
                print(user)
