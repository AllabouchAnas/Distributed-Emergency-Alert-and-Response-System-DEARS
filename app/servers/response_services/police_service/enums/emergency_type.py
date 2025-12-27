from enum import Enum

class EmergencyType(str, Enum):
    POLICE = "POLICE"
    FIRE = "FIRE"
    MEDICAL = "MEDICAL"
