import rpyc
from rpyc.utils.server import ThreadedServer
from .service import MedicalService
from .config import SERVICE_PORT, SERVICE_HOST
from .utils.logger import logger
from .db.db import check_connection

def main():
    logger.info("Starting Medical Service...")
    
    # Check DB connection
    try:
        check_connection()
    except Exception:
        logger.critical("Could not connect to database. Exiting.")
        return

    server = ThreadedServer(
        MedicalService,
        port=SERVICE_PORT,
        hostname=SERVICE_HOST,
        protocol_config={
            'allow_public_attrs': True,
        }
    )
    
    logger.info(f"Medical Service running on {SERVICE_HOST}:{SERVICE_PORT}")
    server.start()

if __name__ == "__main__":
    main()
