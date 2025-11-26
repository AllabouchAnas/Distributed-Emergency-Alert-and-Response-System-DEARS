from enum import Enum

class AlertStatus(str, Enum):
    PENDING = "PENDING"
    ROUTED = "ROUTED"
    ACTIVE = "ACTIVE"
    RESOLVED = "RESOLVED"