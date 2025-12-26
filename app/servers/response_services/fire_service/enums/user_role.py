from enum import Enum

class UserRole(str, Enum):
    CITIZEN = "CITIZEN"
    ADMIN = "ADMIN"
    RESPONDER = "RESPONDER"
