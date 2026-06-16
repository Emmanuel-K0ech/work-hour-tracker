from pydantic import BaseModel

# Structure of data received from the user
class EntryCreate(BaseModel):
    date: str
    hours_worked: float
    hourly_rate: float
