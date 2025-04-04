from sqlalchemy.orm import Session
import models
from typing import Optional

def get_patient_dashboard_info(db: Session, username: str) -> Optional[models.Patient]:
    """
    Fetch patient information for dashboard header based on the database schema:
    - Inherits from BaseUser: id, name, phone, email, password
    - Patient specific: age, blood_group, medical_history
    """
    return db.query(models.Patient)\
             .filter(models.Patient.name == username)\
             .first()

def format_dashboard_response(patient: models.Patient):
    """
    Format patient data for dashboard display
    """
    return {
        "name": patient.name,
        "patient_id": f"Patient ID: P{patient.id:05d}",  # Updated format
        "age": patient.age,
        "blood_group": patient.blood_group,
    }