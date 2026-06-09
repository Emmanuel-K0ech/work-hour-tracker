from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute(
    "SELECT name FROM sqlite_master WHERE type='table';"
)

tables = cursor.fetchall()

print(tables)

conn.close()