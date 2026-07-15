from pydantic import BaseModel

# Structure of data received from the user
class EntryCreate(BaseModel):
    date: str
    hours_worked: float
    hourly_rate: float

# Structure of data sent by the user to update an existing entry
class EntryUpdate(BaseModel):
    hours_worked: float
    hourly_rate: float

# Structure of agent request data
class AgentRequest(BaseModel):
    message: str
