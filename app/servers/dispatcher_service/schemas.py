from pydantic import BaseModel, field_validator
from typing import Optional
from datetime import datetime
from .enums.emergency_type import EmergencyType

class AlertCreate(BaseModel):
    user_id: int
    description: str
    location: str 
    emergency_type: EmergencyType
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    alert_id: Optional[str] = None # UUID passed from client
    
    @field_validator('emergency_type', mode='before')
    @classmethod
    def convert_emergency_type_to_uppercase(cls, v):
        """Convert emergency_type to uppercase if it's a string."""
        if isinstance(v, str):
            return v.upper()
        return v

class AlertResponse(BaseModel):
    alert_id: str
    status: str
    timestamp: datetime
