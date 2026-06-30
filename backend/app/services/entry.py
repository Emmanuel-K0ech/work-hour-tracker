"""
Service functions for managing work entries.
"""

# Saves a work entry to the database
from backend.app.database import get_db_connection


def save_entry(date, hours_worked, hourly_rate):
    # creating database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # checking database for duplicate entries
    cursor.execute(
        """
        SELECT * FROM work_entries
        WHERE date= ?
        """,
        (date,)
    )

    rows = cursor.fetchall()

    # return error if duplicte exists
    if rows:
        return {
            "error": "An entry already exists for this date"
        }
    else:
        cursor.execute("""
        INSERT INTO work_entries
        (date, hours_worked, hourly_rate)
        VALUES (?, ?, ?)
        """,
        (
            date,
            hours_worked,
            hourly_rate
        ))

    conn.commit()

    conn.close()

    return {
        "message": "Entry saved successfully",
        "date": date,
        "hours_worked": hours_worked,
        "hourly_rate": hourly_rate
    }

# retrieve all entries from the database and return them as a list
def get_entries():
    # create database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # select all entries from the database
    cursor.execute("""
    SELECT * FROM work_entries
    """)

    # fetch all rows and return them as a list of dictionaries
    rows = cursor.fetchall()

    conn.close()

    entries = []

    for row in rows:
        entries.append({
            "id": row[0],
            "date": row[1],
            "hours_worked": row[2],
            "hourly_rate": row[3]
        })

    return entries

# retrieve a single entry by its date
def get_entry(date: str):
    # create database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # select entry by date
    cursor.execute("""
    SELECT * FROM work_entries
    WHERE date = ?
    """, (date,))

    # fetch the row and return it as a dictionary
    row = cursor.fetchone()

    conn.close()

    if row:
        return row
    else:
        return {"error": "Entry not found"}

# get summary of a specific from a specific date range
def get_summary(start_date: str, end_date: str):
    # create database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # select entries within the date range
    cursor.execute("""
    SELECT * FROM work_entries
    WHERE date BETWEEN ? AND ?
    """, (start_date, end_date))

    # fetch all rows and return them as a list of dictionaries
    rows = cursor.fetchall()

    conn.close()

    total_hours = 0
    total_earnings = 0

    # calculate total hours and earnings from the entries row by row
    for row in rows:
        total_hours += row[2]
        total_earnings += row[2] * row[3]

    return {
        "start_date": start_date,
        "end_date": end_date,
        "total_hours": total_hours,
        "total_earnings": round(total_earnings, 2)
    }

# update an existing entry by its date
def update_entry(date: str, hours_worked: float, hourly_rate: float):
    # create databse connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # check if entry exists
    cursor.execute("""
    SELECT * FROM work_entries
    WHERE date = ?
    """, (date,))

    row = cursor.fetchone()

    if row:
        # update the entry with new data
        cursor.execute("""
        UPDATE work_entries
        SET hours_worked = ?, hourly_rate = ?
        WHERE date = ?
        """, (hours_worked, hourly_rate, date))
    else:
        return {"error": "Entry not found"}

    conn.commit()
    conn.close()

    return {
            "message": "Entry updated successfully",
            "date": date,
            "hours_worked": hours_worked,
            "hourly_rate": hourly_rate
            }
