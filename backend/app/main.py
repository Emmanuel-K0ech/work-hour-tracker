from app.database import get_db_connection
from app.services.entry import get_entries, save_entry, update_entry, get_summary, get_entry
from fastapi import FastAPI
from app.models import create_tables
from app.schemas import EntryCreate, EntryUpdate, AgentRequest
from app.config import OPENAI_API_KEY
from app.ai import process_message

create_tables()

app = FastAPI()

# Endpoint to create a new entry and save it to the database
#  if entry does not already exist
@app.post("/entries")
def create_entry_endpoint(entry: EntryCreate):
    return save_entry(
        entry.date,
        entry.hours_worked,
        entry.hourly_rate
    )


# retrieve all entries from the database and return them as a list
@app.get("/entries")
def get_entries_endpoint():
    return get_entries()

# retrieve a specific entry by its date and return it
@app.get("/entries/{date}")
def get_entry_endpoint(date: str):
    return get_entry(date)
    
# get summary of of all entries from a specified date range
@app.get("/summary")
def get_summary_endpoint(start_date: str, end_date: str):
    return get_summary(start_date, end_date)

# update an existing entry by its date with new data
@app.put("/entries/{date}")
def update_entry_endpoint(date: str, entry: EntryUpdate):
    return update_entry(
        date,
        entry.hours_worked,
        entry.hourly_rate
    )

# creating an agent endpoint
@app.post("/agent")
def agent_endpoint(request: AgentRequest):
    response = process_message(request.message)
    return { "response": response }

