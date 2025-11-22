from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import DeclarativeBase
from ..config import settings
from ..utils.logger import logger

# 1. Connect to Database
# Build connect_args conditionally based on SSL mode
connect_args = {}
if settings.DB_SSL_MODE and settings.DB_SSL_MODE != "disable":
    connect_args["sslmode"] = settings.DB_SSL_MODE

engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=settings.DB_POOL_SIZE,
    max_overflow=settings.DB_MAX_OVERFLOW,
    pool_timeout=settings.DB_POOL_TIMEOUT,
    future=True,
    connect_args=connect_args if connect_args else {}
)

class Base(DeclarativeBase):
    pass

# 2. Session Factory
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine, 
    future=True
)

# 3. Dependency for FastAPI
def get_db():
    db = SessionLocal()
    try:
        yield db
    except Exception as e:
        logger.error(f"Database transaction error: {e}")
        db.rollback()
        raise e
    finally:
        db.close()


def check_connection():
    try:
        with engine.connect() as conn:
            # Run a simple SQL query that basically says "Hello"
            conn.execute(text("SELECT 1"))
            logger.info("Database connection successful.")
    except Exception as e:
        logger.error(f"Database connection failed: {e}")
        raise e