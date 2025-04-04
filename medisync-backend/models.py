from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from database import Base
from datetime import datetime

class BaseUser(Base):
    __abstract__ = True
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), index=True, nullable=False)
    phone = Column(String(20), unique=True, nullable=False)
    email = Column(String(100), unique=True, nullable=False)
    password = Column(String(100), nullable=False)

    def verify_password(self, password: str) -> bool:
        return self.password == password

class Patient(BaseUser):
    __tablename__ = "patients"
    age = Column(Integer, nullable=False)
    blood_group = Column(String(10), nullable=False)
    medical_history = Column(String(300))
    appointments = relationship("Appointment", back_populates="patient")

class Doctor(BaseUser):
    __tablename__ = "doctors"
    department = Column(String(50), index=True, nullable=False)
    description = Column(Text, nullable=False)
    image_url = Column(
        String(500), 
        default="https://placehold.co/300x200",
        nullable=False
    )
    appointments = relationship("Appointment", back_populates="doctor")

    def to_response(self):
        """Convert to response format needed by frontend"""
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "description": self.description,
            "image_url": self.image_url
        }

class Admin(BaseUser):
    __tablename__ = "admins"
    department = Column(String(50), nullable=True)

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_id = Column(Integer, ForeignKey("patients.id"), nullable=False)
    doctor_id = Column(Integer, ForeignKey("doctors.id"), nullable=False)
    appointment_time = Column(DateTime, nullable=False)
    status = Column(String(50), nullable=False, default="pending")

    patient = relationship("Patient", back_populates="appointments")
    doctor = relationship("Doctor", back_populates="appointments")