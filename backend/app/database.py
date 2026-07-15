import sqlite3
from pathlib import Path


BASE_DIR = Path(__file__).resolve().parent

DATABASE = BASE_DIR / "timetracker.db"


def get_db_connection():

    connection = sqlite3.connect(DATABASE)

    connection.row_factory = sqlite3.Row

    return connection
