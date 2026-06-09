import sqlite3

DATABASE_NAME = 'timetracker.db'

def get_db_connection():
    return sqlite3.connect(DATABASE_NAME)
