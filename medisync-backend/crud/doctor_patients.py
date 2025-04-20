from sqlalchemy.orm import Session
from sqlalchemy import distinct
import models
from typing import List

def get_doctor_by_name(db: Session, username: str):
    """
    Fetch doctor information by username
    """
    return db.query(models.Doctor)\
             .filter(models.Doctor.name == username)\
             .first()

def get_doctor_patients(db: Session, doctor_id: int) -> List[models.Patient]:
    """
    Fetch all patients who have appointments with the doctor
    Returns unique patients even if they have multiple appointments
    """
    return db.query(models.Patient)\
             .join(models.Appointment)\
             .filter(models.Appointment.doctor_id == doctor_id)\
             .distinct()\
             .all()

def format_patients_response(patients: List[models.Patient]):
    """
    Format all patients for display
    """
    return {
        "patients": [
            {
                "patient_id": f"P{patient.id:05d}",
                "name": patient.name,
                "email": patient.email,
                "phone": patient.phone,
                "last_visit": max([apt.appointment_time for apt in patient.appointments]).strftime("%Y-%m-%d %H:%M:%S") if patient.appointments else "No visits",
                "total_visits": len(patient.appointments)
            }
            for patient in patients
        ]
    }