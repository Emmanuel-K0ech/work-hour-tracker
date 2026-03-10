from sqlalchemy import Column, Integer, DateTime, Float
from datetime import datetime
from database import Base

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    clock_in = Column(DateTime, default=datetime.now)
    clock_out = Column(DateTime, nullable=True)
    hours_worked = Column(Float, nullable=True)
