from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute(
    "SELECT * FROM work_entries"
)

rows = cursor.fetchall()

print(rows)

conn.close()