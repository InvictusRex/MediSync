from sqlalchemy.orm import Session
from models import Doctor
from schemas import DoctorHeaderResponse

def get_doctor_dashboard_info(db: Session, username: str) -> DoctorHeaderResponse:
    """
    Fetch doctor information for dashboard header
    """
    doctor = db.query(Doctor).filter(Doctor.name == username).first()
    if not doctor:
        return None

    return DoctorHeaderResponse(
        name=doctor.name,
        doctor_id=f"Doctor ID: D{doctor.id:05d}",
        department=doctor.department
    )