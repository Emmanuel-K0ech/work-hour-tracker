from app.database import get_db_connection


def create_tables():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS work_entries (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            date TEXT NOT NULL,
            hours_worked REAL NOT NULL,
            hourly_rate REAL NOT NULL
        )
    ''')
    conn.commit()
    conn.close()