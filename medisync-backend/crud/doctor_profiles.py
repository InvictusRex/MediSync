from sqlalchemy.orm import Session
import models
from typing import Optional

def get_doctor_profile(db: Session, username: str) -> Optional[models.Doctor]:
    """
    Fetch doctor profile information
    """
    return db.query(models.Doctor)\
             .filter(models.Doctor.name == username)\
             .first()

def format_profile_response(doctor: models.Doctor):
    """
    Format doctor data for profile display
    """
    return {
        "header": f"Dr. {doctor.name}'s Profile",
        "doctor_info": {
            "ID": f"D{doctor.id:05d}",
            "Name": doctor.name,
            "Department": doctor.department,
            "Email": doctor.email,
            "Phone": doctor.phone,
            "Description": doctor.description
        }
    }