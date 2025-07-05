# Python Generators 0x00

This project demonstrates the use of Python generators to stream data from a MySQL database.

## Files

- `0-main.py`: Main script to test the database connection and data insertion.
- `seed.py`: Module to set up and populate the `ALX_prodev` database.
- `user_data.csv`: Sample data to be inserted into the database.
- `README.md`: This file.

## Requirements

- Python 3
- MySQL server
- `mysql-connector-python` library

## Setup

1. **Install the required library:**
   ```bash
   pip install mysql-connector-python
   ```

2. **Start your MySQL server.**

3. **Run the main script:**
   ```bash
   ./0-main.py
   ```

## Database Schema

- **Database:** `ALX_prodev`
- **Table:** `user_data`
  - `user_id` (VARCHAR(255), PRIMARY KEY)
  - `name` (VARCHAR(255), NOT NULL)
  - `email` (VARCHAR(255), NOT NULL)
  - `age` (DECIMAL, NOT NULL)