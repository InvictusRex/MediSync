from sqlalchemy import Column, Integer, String, Text, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
from database import get_formatted_time

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
    role = Column(String(20), default="patient")
    last_login = Column(DateTime, default=datetime.utcnow)

    def verify_password(self, password: str) -> bool:
        return self.password == password

    def get_dashboard_info(self) -> dict:
        """Get formatted user info for dashboard"""
        return {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "blood_group": self.blood_group,
            "medical_history": self.medical_history,
            "phone": self.phone,
            "email": self.email,
            "role": self.role,
            "last_login": get_formatted_time(self.last_login) if self.last_login else None
        }

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department = Column(String(50), index=True)
    description = Column(Text)
    image_url = Column(String(500), default="https://placehold.co/300x200")
    created_at = Column(DateTime, default=datetime.utcnow)

    def get_info(self) -> dict:
        """Get formatted doctor info"""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "description": self.description,
            "image_url": self.image_url,
            "created_at": get_formatted_time(self.created_at) if self.created_at else None
        }

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), index=True)
    doctor_name = Column(String(100), index=True)
    appointment_date = Column(DateTime, nullable=False)
    status = Column(String(50))
    created_at = Column(DateTime, default=datetime.utcnow)

    def get_formatted_info(self) -> dict:
        """Get formatted appointment info for dashboard"""
        return {
            "id": self.id,
            "doctor_name": self.doctor_name,
            "date": get_formatted_time(self.appointment_date) if self.appointment_date else None,
            "status": self.status
        }

# Database engine and session configuration
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create all tables in the database
Base.metadata.create_all(bind=engine)