#!/usr/bin/python3
"""
This module provides functions to set up and populate the ALX_prodev database.
"""
import uuid
import mysql.connector
import csv
import os

def connect_db():
    """Connects to the MySQL database server."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testpassword'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to MySQL: {err}")
        return None

def create_database(connection):
    """Creates the database ALX_prodev if it does not exist."""
    try:
        cursor = connection.cursor()
        cursor.execute("CREATE DATABASE IF NOT EXISTS ALX_prodev")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating database: {err}")

def connect_to_prodev():
    """Connects to the ALX_prodev database in MySQL."""
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='testpassword',
            database='ALX_prodev'
        )
        return connection
    except mysql.connector.Error as err:
        print(f"Error connecting to database ALX_prodev: {err}")
        return None

def create_table(connection):
    """Creates a table user_data if it does not exist with the required fields."""
    try:
        cursor = connection.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS user_data (
                user_id VARCHAR(255) PRIMARY KEY,
                name VARCHAR(255) NOT NULL,
                email VARCHAR(255) NOT NULL,
                age DECIMAL NOT NULL
            )
        """)
        print("Table user_data created successfully")
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error creating table: {err}")

def insert_data(connection, data_file):
    """Inserts data in the database if it does not exist."""
    try:
        cursor = connection.cursor()
        with open(data_file, 'r') as csvfile:
            csvreader = csv.reader(csvfile)
            next(csvreader)  # Skip header row
            for row in csvreader:
                name, email, age = row
                # Check if email already exists
                cursor.execute("SELECT email FROM user_data WHERE email = %s", (email,))
                if not cursor.fetchone():
                    user_id = str(uuid.uuid4()) 
                    sql = "INSERT INTO user_data (user_id, name, email, age) VALUES (%s, %s, %s, %s)"
                    val = (user_id, name, email, age)
                    cursor.execute(sql, val)
        connection.commit()
        cursor.close()
    except mysql.connector.Error as err:
        print(f"Error inserting data: {err}")
    except FileNotFoundError:
        print(f"Error: Data file '{data_file}' not found.")