from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine

# Database configuration
DATABASE_URL = "mysql+mysqlconnector://TheKingslayer:rupankar@localhost/medisync"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    blood_group = Column(String(10))
    medical_history = Column(String(300))
    phone = Column(String(20), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))
    role = Column(String(20), default="patient")  # Added role column for authentication

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored password"""
        return self.password == password

# In models.py
class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department = Column(String(50), index=True)
    description = Column(Text)
    image_url = Column(String(500), default="https://placehold.co/300x200")  # Default placeholder

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), index=True)
    time = Column(String(50))
    status = Column(String(50))

# Database engine and session configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)