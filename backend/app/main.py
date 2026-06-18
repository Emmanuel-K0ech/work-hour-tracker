from database import get_db_connection
from fastapi import FastAPI
from models import create_tables
from schemas import EntryCreate

create_tables()

app = FastAPI()

# Endpoint to create a new entry and save it to the database
#  if entry does not already exist
@app.post("/entries")
def create_entry(entry: EntryCreate):

    # creating database connection
    conn = get_db_connection()
    cursor = conn.cursor()

    # checking database for duplicate entries
    cursor.execute(
        """
        SELECT * FROM work_entries
        WHERE date= ?
        """,
        (entry.date,)
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
            entry.date,
            entry.hours_worked,
            entry.hourly_rate
        ))

    conn.commit()

    conn.close()

    return {
        "message": "Entry saved successfully",
        "date": entry.date,
        "hours_worked": entry.hours_worked,
        "hourly_rate": entry.hourly_rate
    }


# retrieve all entries from the database and return them as a list
@app.get("/entries")
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


# retrieve a specific entry by its date and return it
@app.get("/entries/{date}")
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

# get summary of of all entries from a specified date range
@app.get("/summary")
def get_summary(start_date: str, end_date: str):
    pass

# update an existing entry by its date with new data
@app.put("/entries/{date}")
def update_entry(date: str):
    pass