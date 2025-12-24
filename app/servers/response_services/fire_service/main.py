import rpyc
from rpyc.utils.server import ThreadedServer
from .service import FireService
from .config import SERVICE_PORT, SERVICE_HOST
from .utils.logger import logger
from .db.db import check_connection

def main():
    logger.info("Starting Fire Service...")
    
    # Check DB connection
    try:
        check_connection()
    except Exception:
        logger.critical("Could not connect to database. Exiting.")
        return

    server = ThreadedServer(
        FireService,
        port=SERVICE_PORT,
        hostname=SERVICE_HOST,
        protocol_config={
            'allow_public_attrs': True,
        }
    )
    
    logger.info(f"Fire Service running on {SERVICE_HOST}:{SERVICE_PORT}")
    server.start()

if __name__ == "__main__":
    main()
