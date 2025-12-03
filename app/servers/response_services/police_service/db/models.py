from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .db import Base

class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, nullable=False) 
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default="PENDING")
    emergency_type = Column(String(32), nullable=False)  
    assigned_unit = Column(Integer, nullable=True) 


class ResponseUnit(Base):
    __tablename__ = "response_units"

    unit_id = Column(Integer, primary_key=True, index=True)
    unit_name = Column(String(120), nullable=False) 
    unit_type = Column(String(32), nullable=False) 
    current_location = Column(String(255), nullable=False)
    status = Column(String(32), nullable=False, default="AVAILABLE")


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(String(32), nullable=False, default="CITIZEN")  
