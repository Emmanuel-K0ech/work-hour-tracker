from sqlalchemy import Column, Integer, DateTime, Float, String, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from .database import Base

class Role(Base):
    __tablename__ = "roles"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    hourly_rate = Column(Float)
    shifts = relationship("Shift", back_populates="role_obj")

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    clock_in = Column(DateTime, default=datetime.now)
    clock_out = Column(DateTime, nullable=True)
    hours_worked = Column(Float, nullable=True)
    location = Column(String, index=True)
    role_id = Column(Integer, ForeignKey("roles.id"))
    role_obj = relationship("Role", back_populates="shifts")
    pay = Column(Float, nullable=True)
