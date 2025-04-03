from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager
from datetime import datetime

# Database connection URL
# Format: mysql+mysqlconnector://username:password@host/database_name
DATABASE_URL = "mysql+mysqlconnector://TheKingslayer:rupankar@localhost/medisync"

# Create database engine with connection pool settings
engine = create_engine(
    DATABASE_URL,
    pool_size=5,  # Number of connections to maintain in the pool
    max_overflow=10,  # Maximum number of connections that can be created beyond pool_size
    pool_timeout=30,  # Seconds to wait before giving up on getting a connection from the pool
    pool_recycle=1800  # Recycle connections after 30 minutes to prevent stale connections
)

# Create SessionLocal class for database sessions
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()

@contextmanager
def get_db():
    """
    Context manager for database sessions.
    Ensures proper handling of sessions and automatic closing.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_formatted_time(dt: datetime = None):
    """
    Format a datetime object to consistent UTC string
    If no datetime provided, uses current time
    """
    if dt is None:
        dt = datetime.utcnow()
    return dt.strftime("%Y-%m-%d %H:%M:%S UTC")

def init_db():
    """
    Initialize database by creating all tables
    """
    Base.metadata.create_all(bind=engine)

# Optional: Add connection testing
def test_connection():
    """
    Test database connection
    """
    try:
        with get_db() as db:
            db.execute("SELECT 1")
        return True
    except Exception as e:
        print(f"Database connection failed: {str(e)}")
        return False

# Initialize database on import
init_db()