from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from .enums.emergency_type import EmergencyType

class AlertCreate(BaseModel):
    user_id: int
    description: str
    location: str 
    emergency_type: EmergencyType
    
    

class AlertResponse(BaseModel):
    alert_id: str  # UUID string
    status: str
    timestamp: datetime
    
    class Config:
        from_attributes = True
