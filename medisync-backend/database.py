from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Database connection URL
# Format: mysql+mysqlconnector://username:password@host/database_name
DATABASE_URL = "mysql+mysqlconnector://TheKingslayer:rupankar@localhost/medisync"

# Create database engine
engine = create_engine(DATABASE_URL)

# Create SessionLocal class for database sessions
# autocommit=False: Transactions must be committed explicitly
# autoflush=False: Changes won't be flushed to DB automatically
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create base class for declarative models
Base = declarative_base()