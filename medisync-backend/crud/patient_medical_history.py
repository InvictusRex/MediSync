from sqlalchemy.orm import Session
import models
from typing import Optional, List
from datetime import datetime

def get_patient_medical_history_info(db: Session, username: str) -> Optional[models.Patient]:
    """
    Fetch patient information for medical history page
    """
    return db.query(models.Patient)\
             .filter(models.Patient.name == username)\
             .first()

def get_patient_appointments(db: Session, patient_id: int) -> List[models.Appointment]:
    """
    Fetch all appointments for the patient
    """
    return db.query(models.Appointment)\
             .filter(models.Appointment.patient_id == patient_id)\
             .all()

def format_medical_history_response(patient: models.Patient, appointments: List[models.Appointment]):
    """
    Format patient data and appointments for medical history display
    """
    return {
        "name": patient.name,
        "patient_id": f"Patient ID: P{patient.id:05d}",
        "appointments": [
            {
                "appointment_id": appointment.id,
                "date_time": appointment.appointment_time.strftime("%Y-%m-%d %H:%M"),
                "doctor": f"Dr. {appointment.doctor.name}",
                "status": appointment.status
            }
            for appointment in appointments
        ]
    }