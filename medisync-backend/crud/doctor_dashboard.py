from sqlalchemy.orm import Session
from sqlalchemy import asc
import models
from typing import List
from datetime import datetime

def get_doctor_appointments(db: Session, doctor_id: int, limit: int = 10) -> List[models.Appointment]:
    """
    Fetch pending appointments for a doctor in ascending order of date/time
    """
    return db.query(models.Appointment)\
             .filter(models.Appointment.doctor_id == doctor_id)\
             .filter(models.Appointment.status == "pending")\
             .order_by(asc(models.Appointment.appointment_time))\
             .limit(limit)\
             .all()

def get_doctor_by_name(db: Session, username: str):
    """
    Fetch doctor information by username
    """
    return db.query(models.Doctor)\
             .filter(models.Doctor.name == username)\
             .first()

def format_dashboard_response(appointments: List[models.Appointment]):
    """
    Format appointments for dashboard display
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

def update_appointment(db: Session, appointment_id: int, new_datetime: datetime = None, new_status: str = None):
    """
    Update appointment datetime and/or status
    """
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if not appointment:
        return None
    
    if new_datetime:
        appointment.appointment_time = new_datetime
    if new_status:
        appointment.status = new_status
    
    db.commit()
    db.refresh(appointment)
    return appointment