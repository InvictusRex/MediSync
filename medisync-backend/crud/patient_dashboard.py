from sqlalchemy.orm import Session
import models
from typing import Optional, List
from datetime import datetime

def get_patient_dashboard_info(db: Session, username: str) -> Optional[models.Patient]:
    """
    Fetch patient information for dashboard page
    """
    return db.query(models.Patient)\
             .filter(models.Patient.name == username)\
             .first()

def get_recent_appointments(db: Session, patient_id: int) -> List[models.Appointment]:
    """
    Fetch the 5 most recent appointments for the patient
    """
    return db.query(models.Appointment)\
             .filter(models.Appointment.patient_id == patient_id)\
             .order_by(models.Appointment.appointment_time.desc())\
             .limit(5)\
             .all()

def format_dashboard_response(patient: models.Patient, appointments: List[models.Appointment]):
    """
    Format patient data and appointments for dashboard display
    """
    return {
        "name": patient.name,
        "patient_id": f"Patient ID: P{patient.id:05d}",
        "recent_appointments": [  # Changed back to recent_appointments to match schema
            {
                "appointment_id": appointment.id,
                "date_time": appointment.appointment_time.strftime("%Y-%m-%d %H:%M"),
                "doctor": f"Dr. {appointment.doctor.name}",
                "status": appointment.status
            }
            for appointment in appointments
        ]
    }