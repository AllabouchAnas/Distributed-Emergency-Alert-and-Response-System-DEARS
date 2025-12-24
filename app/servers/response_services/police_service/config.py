import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings:

    DATABASE_URL = os.getenv("DATABASE_URL")
    if not DATABASE_URL:
        # Fallback for dev if not set, though it should be set in .env
        pass
    
    DB_SSL_MODE = os.getenv("DB_SSL_MODE", "disable")
    
    DB_POOL_SIZE = 5
    DB_MAX_OVERFLOW = 10
    DB_POOL_TIMEOUT = 30 

settings = Settings()

SERVICE_PORT = int(os.getenv("POLICE_SERVICE_PORT", "9001"))
SERVICE_HOST = os.getenv("POLICE_SERVICE_HOST", "0.0.0.0")
