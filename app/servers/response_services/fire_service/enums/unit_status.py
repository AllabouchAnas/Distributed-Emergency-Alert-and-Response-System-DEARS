from enum import Enum

class UnitStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    EN_ROUTE = "EN_ROUTE"
    ON_SCENE = "ON_SCENE"
    UNAVAILABLE = "UNAVAILABLE"
