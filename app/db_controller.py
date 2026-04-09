# THIS IS BACKUP FILE
# WHILE USING (SQLite) , THIS FILE HAS FUNCTION OF DATABASE BACKUP FILE
# In case DB would crash, dev can use this file to reconstruct db using functions and SQL query

import sqlite3
import os

from dotenv import load_dotenv
from parser import data_parser

# Loading environments variables: URL
load_dotenv()

url = os.getenv("url")

# Parse data from URL, and formate it
data = data_parser(url)

def db_insert(full):
    # Connecting to DB
    conn = sqlite3.connect("data.db")
    cursor = conn.cursor()

    # Creating a table if it not exist
    cursor.execute('''CREATE TABLE IF NOT EXISTS flats (
                link TEXT UNIQUE,
                price REAL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        ''')

    # Write data from Parser down
    for p, l in full:
        cursor.execute("INSERT INTO flats (link, price) VALUES (?,?)", (l, p))

    # Commiting changes and close connection
    conn.commit()
    conn.close()


# IN CASE YOU WANT TO RECONSTRUCT DB, UNCOMMENT THIS SECTION AND START FILE

# if __name__ == '__main__':
#     db_insert(data)



