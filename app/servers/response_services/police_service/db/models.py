from sqlalchemy import Column, Integer, String, DateTime, Text, Float, Enum as SQLEnum
from sqlalchemy.sql import func
from sqlalchemy.dialects.postgresql import UUID
from .db import Base
from ..enums import AlertStatus, EmergencyType, UnitStatus, UserRole


class User(Base):
    __tablename__ = "users"

    user_id = Column(Integer, primary_key=True, index=True)
    username = Column(String(100), nullable=False, unique=True)
    password_hash = Column(Text, nullable=False)
    role = Column(SQLEnum(UserRole), nullable=False, default=UserRole.CITIZEN)


class Alert(Base):
    __tablename__ = "alerts"

    alert_id = Column(Integer, primary_key=True, index=True)
    alert_uuid = Column(UUID(as_uuid=True), unique=True, nullable=True) # UUID type
    user_id = Column(Integer, nullable=False)
    timestamp = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
    description = Column(Text, nullable=False)
    location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(SQLEnum(AlertStatus), nullable=False, default=AlertStatus.PENDING)
    emergency_type = Column(SQLEnum(EmergencyType), nullable=False)
    assigned_unit = Column(Integer, nullable=True)


class ResponseUnit(Base):
    __tablename__ = "response_units"

    unit_id = Column(Integer, primary_key=True, index=True)
    unit_name = Column(String(120), nullable=False)
    unit_type = Column(SQLEnum(EmergencyType), nullable=False)
    current_location = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=True)
    longitude = Column(Float, nullable=True)
    status = Column(SQLEnum(UnitStatus), nullable=False, default=UnitStatus.AVAILABLE)
