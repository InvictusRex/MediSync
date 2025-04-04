from sqlalchemy.orm import Session
import models
from typing import Optional
from datetime import datetime

def get_patient_profile(db: Session, username: str) -> Optional[models.Patient]:
    """
    Fetch patient profile information matching the database schema
    """
    return db.query(models.Patient)\
             .filter(models.Patient.name == username)\
             .first()

def format_profile_response(patient: models.Patient):
    """
    Format patient data for profile display based on actual database schema
    """
    return {
        "header": f"Current Date and Time (UTC - YYYY-MM-DD HH:MM:SS formatted): {datetime.utcnow().strftime('%Y-%m-%d %H:%M:%S')}\nCurrent User's Login: {patient.name}",
        "patient_info": {
            "name": patient.name,
            "patient_id": f"P{patient.id:05d}",
            "email": patient.email,
            "phone": patient.phone,
            "age": patient.age,
            "blood_group": patient.blood_group,
            "medical_history": patient.medical_history or "No medical history available"
        }
    }