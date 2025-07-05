#!/usr/bin/python3
"""
This module contains a generator to stream user ages and calculate the average.
"""
from seed import connect_to_prodev
import mysql.connector

def stream_user_ages():
    """Yields user ages one by one from the database."""
    connection = connect_to_prodev()
    if not connection:
        return

    try:
        cursor = connection.cursor(dictionary=True)
        cursor.execute("SELECT age FROM user_data")
        for row in cursor:
            yield row['age']
    except mysql.connector.Error as err:
        print(f"Error: {err}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

def calculate_average_age():
    """Calculates the average age from the streamed user ages."""
    total_age = 0
    user_count = 0
    for age in stream_user_ages():
        total_age += age
        user_count += 1
    
    if user_count > 0:
        average_age = total_age / user_count
        print(f"Average age of users: {average_age:.2f}")
    else:
        print("No users found to calculate average age.")

if __name__ == "__main__":
    calculate_average_age()
