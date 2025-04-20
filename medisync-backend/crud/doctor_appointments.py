from sqlalchemy.orm import Session
from sqlalchemy import desc
import models
from typing import List
from datetime import datetime

def get_doctor_by_name(db: Session, username: str):
    """
    Fetch doctor information by username
    """
    return db.query(models.Doctor)\
             .filter(models.Doctor.name == username)\
             .first()

def get_all_doctor_appointments(db: Session, doctor_id: int) -> List[models.Appointment]:
    """
    Fetch all appointments for a doctor, ordered by date
    Returns all appointments regardless of status
    """
    return db.query(models.Appointment)\
             .filter(models.Appointment.doctor_id == doctor_id)\
             .order_by(models.Appointment.appointment_time.asc())\
             .all()

def format_appointments_response(appointments: List[models.Appointment]):
    """
    Format all appointments for display
    """
    return {
        "appointments": [
            {
                "appointment_id": f"A{appointment.id:05d}",
                "date_time": appointment.appointment_time.strftime("%Y-%m-%d %H:%M:%S"),
                "patient_id": f"P{appointment.patient.id:05d}",
                "patient_name": appointment.patient.name,
                "status": appointment.status,
            }
            for appointment in appointments
        ]
    }