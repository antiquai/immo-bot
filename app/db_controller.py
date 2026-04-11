# THIS IS BACKUP FILE
# WHILE USING (SQLite) , THIS FILE HAS FUNCTION OF DATABASE BACKUP FILE
# In case DB would crash, dev can use this file to reconstruct db using functions and SQL query

import sqlite3
import os

from dotenv import load_dotenv
from parser import data_parser as d_p

normalize_db_path = os.path.dirname(os.path.abspath(__file__))

# Loading environments variables: URL
load_dotenv()

url = os.getenv("url")

def db_insert(full):
    # Connecting to DB
    db_path = os.path.join(normalize_db_path, "data.db")
    with sqlite3.connect(db_path) as conn:
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



# Fetching recent list from Database ---
def fetch_data(link):
    # Try setch data from DB. If there no DB use function from __db_controller.py__
    db_path = os.path.join(normalize_db_path, "data.db")

    def get_records():
        with sqlite3.connect(db_path) as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM flats')
            return cursor.fetchall()

    try:
        return get_records()

    except (sqlite3.OperationalError, sqlite3.DatabaseError):
        db_insert(d_p(link))
        return get_records()


# New Solving ---
def sync_with_site(link):
    data = d_p(link)
    db_path = os.path.join(normalize_db_path, "data.db")

    new_records = []

    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()
        for price, href in data:
            cursor.execute('SELECT * FROM flats WHERE link = ?', (href,))
            exists = cursor.fetchone()

        if not exists:
            cursor.execute('INSERT INTO flats (link, price) VALUES (?, ?)', (href, price))
            new_records.append((href, price))

    return new_records

def fetch_latest_flats(lim):
    db_path = os.path.join(normalize_db_path, "data.db")
    with sqlite3.connect(db_path) as conn:
        cursor = conn.cursor()

        # Search every element in arrange of (maybe) new founded links
        cursor.execute("""
            SELECT link, price, created_at
            FROM flats
            ORDER BY created_at DESC
            LIMIT ?
        """, (lim,))

        data = cursor.fetchall()

    return data


# IN CASE YOU WANT TO RECONSTRUCT DB, UNCOMMENT THIS SECTION AND START FILE

# if __name__ == '__main__':
#     db_insert(d_p(url))



