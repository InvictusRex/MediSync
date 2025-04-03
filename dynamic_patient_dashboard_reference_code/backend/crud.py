from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from datetime import datetime
import models
import schemas
from database import get_formatted_time  # Import the formatting function

# User related operations
def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()

def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        age=user.age,
        blood_group=user.blood_group,
        medical_history=user.medical_history,
        phone=user.phone,
        email=user.email,
        password=user.password,
        role=user.role
    )
    db.add(db_user)
    try:
        db.commit()
        db.refresh(db_user)
        return db_user
    except Exception as e:
        db.rollback()
        raise e

def verify_user(db: Session, identifier: str, password: str, role: str):
    """
    Verify user login credentials and role
    """
    user = db.query(models.User).filter(
        or_(
            models.User.email == identifier,
            models.User.phone == identifier
        )
    ).first()
    
    if not user:
        return None
    
    if user.password == password and user.role == role:
        return user
    
    return None

def get_patient_dashboard_data(db: Session, user_id: int):
    """
    Get complete patient dashboard data including profile and appointments
    """
    user = get_user(db, user_id)
    if not user:
        return None

    # Get recent appointments
    appointments = get_recent_appointments(db, user_id, limit=10)

    dashboard_data = {
        "system_info": {
            "timestamp": get_formatted_time(),
            "user_login": user.name
        },
        "profile": {
            "id": user.id,
            "name": user.name,
            "age": user.age,
            "blood_group": user.blood_group,
            "medical_history": user.medical_history,
            "phone": user.phone,
            "email": user.email
        },
        "appointments": [
            {
                "id": apt.id,
                "doctor_name": apt.doctor_name,
                "date": get_formatted_time(apt.appointment_date) if hasattr(apt, 'appointment_date') else apt.time,
                "status": apt.status
            } for apt in appointments
        ]
    }
    
    return dashboard_data

def get_user_profile(db: Session, user_id: int):
    """
    Get complete user profile including appointments and medical history
    """
    user = get_user(db, user_id)
    if not user:
        return None
    
    user_data = {
        "id": user.id,
        "name": user.name,
        "email": user.email,
        "phone": user.phone,
        "age": user.age,
        "blood_group": user.blood_group,
        "medical_history": user.medical_history,
        "role": user.role,
        "last_login": get_formatted_time(datetime.utcnow())
    }
    
    recent_appointments = get_recent_appointments(db, user_id)
    user_data["appointments"] = [
        {
            "id": apt.id,
            "doctor_name": apt.doctor_name,
            "date": get_formatted_time(apt.appointment_date) if hasattr(apt, 'appointment_date') else apt.time,
            "status": apt.status
        } for apt in recent_appointments
    ]
    
    return user_data