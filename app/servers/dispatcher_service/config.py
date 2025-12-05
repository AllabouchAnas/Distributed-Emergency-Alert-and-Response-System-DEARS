import os
from dotenv import load_dotenv

load_dotenv(os.path.join(os.path.dirname(__file__), ".env"))

DISPATCHER_HOST = os.getenv("DISPATCHER_HOST", "0.0.0.0")
DISPATCHER_PORT = int(os.getenv("DISPATCHER_PORT", "8000"))

RPC_SERVICES = {
    "POLICE": {"host": os.getenv("RPC_POLICE_HOST", "localhost"),
               "port": int(os.getenv("RPC_POLICE_PORT", "9001"))},
    "FIRE": {"host": os.getenv("RPC_FIRE_HOST", "localhost"),
             "port": int(os.getenv("RPC_FIRE_PORT", "9002"))},
    "MEDICAL": {"host": os.getenv("RPC_MEDICAL_HOST", "localhost"),
                "port": int(os.getenv("RPC_MEDICAL_PORT", "9003"))},
}

RPC_CALLBACK_HOST = os.getenv("RPC_CALLBACK_HOST", "0.0.0.0")
RPC_CALLBACK_PORT = int(os.getenv("RPC_CALLBACK_PORT", "18000"))

RPC_RETRIES = int(os.getenv("RPC_RETRIES", "2"))
RPC_TIMEOUT = int(os.getenv("RPC_TIMEOUT", "5"))
