from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base
from database import Base  # Import Base from database.py

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

    def verify_password(self, password: str) -> bool:
        """Verify if the provided password matches the stored password"""
        return self.password == password

class Doctor(Base):
    __tablename__ = "doctors"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True)
    department = Column(String(50), index=True)
    description = Column(Text)
    image_url = Column(String(500), default="https://placehold.co/300x200")

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), index=True)
    time = Column(String(50))
    status = Column(String(50))
