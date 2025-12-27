import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

class Settings:
    # Database Settings
    DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://user:password@localhost/dears_db")
    DB_SSL_MODE = os.getenv("DB_SSL_MODE", "disable")
    DB_POOL_SIZE = int(os.getenv("DB_POOL_SIZE", "5"))
    DB_MAX_OVERFLOW = int(os.getenv("DB_MAX_OVERFLOW", "10"))
    DB_POOL_TIMEOUT = int(os.getenv("DB_POOL_TIMEOUT", "30"))

    # Dispatcher Settings
    DISPATCHER_HOST = os.getenv("DISPATCHER_HOST", "0.0.0.0")
    DISPATCHER_PORT = int(os.getenv("DISPATCHER_PORT", "8001"))

    # RPC Configuration
    RPC_CALLBACK_HOST = os.getenv("RPC_CALLBACK_HOST", "0.0.0.0")
    RPC_CALLBACK_PORT = int(os.getenv("RPC_CALLBACK_PORT", "18000"))
    RPC_RETRIES = int(os.getenv("RPC_RETRIES", "2"))
    RPC_TIMEOUT = int(os.getenv("RPC_TIMEOUT", "5"))

settings = Settings()

# Individual Variables (for compatibility with existing code)
DISPATCHER_HOST = settings.DISPATCHER_HOST
DISPATCHER_PORT = settings.DISPATCHER_PORT
RPC_CALLBACK_HOST = settings.RPC_CALLBACK_HOST
RPC_CALLBACK_PORT = settings.RPC_CALLBACK_PORT
RPC_RETRIES = settings.RPC_RETRIES
RPC_TIMEOUT = settings.RPC_TIMEOUT

RPC_SERVICES = {
    "POLICE": [],
    "FIRE": [],
    "MEDICAL": [],
}

# Helper function to load service configurations
def load_services(service_type, env_prefix, default_port):
    # Always try to load the primary service
    host = os.getenv(f"{env_prefix}_HOST", "localhost")
    port = int(os.getenv(f"{env_prefix}_PORT", str(default_port)))
    RPC_SERVICES[service_type].append({"host": host, "port": port})

    # Try to load additional services (up to 5 for now)
    for i in range(2, 6):
        host_key = f"{env_prefix}_HOST_{i}"
        port_key = f"{env_prefix}_PORT_{i}"
        
        if os.getenv(host_key) or os.getenv(port_key):
            host = os.getenv(host_key, "localhost")
            port = int(os.getenv(port_key, str(default_port + i - 1))) # Default port increment just in case
            RPC_SERVICES[service_type].append({"host": host, "port": port})

load_services("POLICE", "RPC_POLICE", 9001)
load_services("FIRE", "RPC_FIRE", 9002)
load_services("MEDICAL", "RPC_MEDICAL", 9003)
