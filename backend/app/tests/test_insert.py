from database import get_db_connection

conn = get_db_connection()

cursor = conn.cursor()

cursor.execute("""
INSERT INTO work_entries
(date, hours_worked, hourly_rate)
VALUES (?, ?, ?)
""", ("2026-05-23", 6.44, 10.00))

conn.commit()

conn.close()

print("Record inserted")