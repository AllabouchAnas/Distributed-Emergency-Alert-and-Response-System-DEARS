import rpyc
from rpyc.utils.server import ThreadedServer
from .service import PoliceService
from .config import SERVICE_PORT, SERVICE_HOST
from .utils.logger import logger
from .db.db import check_connection

def main():
    logger.info("Starting Police Service...")
    
    # Check DB connection
    # Check DB connection and create tables (for SQLite/Dev)
    try:
        check_connection()
        from .db.db import engine, Base
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created (if not exist).")
    except Exception as e:
        logger.critical(f"Could not connect to database: {e}. Exiting.")
        return

    server = ThreadedServer(
        PoliceService,
        port=SERVICE_PORT,
        hostname=SERVICE_HOST,
        protocol_config={
            'allow_public_attrs': True,
        }
    )
    
    logger.info(f"Police Service running on {SERVICE_HOST}:{SERVICE_PORT}")
    server.start()

if __name__ == "__main__":
    main()
