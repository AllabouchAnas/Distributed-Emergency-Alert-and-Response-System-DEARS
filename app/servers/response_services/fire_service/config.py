import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        pass
    
    DB_SSL_MODE = os.getenv("DB_SSL_MODE", "disable")
    
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
    DB_POOL_TIMEOUT = 30 

settings = Settings()

SERVICE_PORT = int(os.getenv("FIRE_SERVICE_PORT", "9002"))
SERVICE_HOST = os.getenv("FIRE_SERVICE_HOST", "0.0.0.0")
