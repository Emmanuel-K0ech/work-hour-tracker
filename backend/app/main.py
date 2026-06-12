from fastapi import FastAPI
from models import create_entry

create_entry()

app = FastAPI()

# Endpoint to create a new entry and save it to the database
#  if entry does not already exist
@app.post("/entries")
def create_entry():
    pass

# retrieve all entries from the database and return them as a list
@app.get("/entries")
def get_entries():
    pass

# retrieve a specific entry by its ID and return it
@app.get("/entries/{date}")
def get_entry(entry_id: int):
    pass

# get summary of of all entries from a specidied date range
@app.get("/summary")
def get_summary(start_date: str, end_date: str):
    pass

# update an existing entry by its date with new data
@app.put("/entries/{date}")
def update_entry(date: str):
    pass