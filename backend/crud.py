from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()

def get_user_by_phone(db: Session, phone: str):
    return db.query(models.User).filter(models.User.phone == phone).first()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(
        name=user.name,
        age=user.age,
        blood_group=user.blood_group,
        medical_history=user.medical_history,
        phone=user.phone,
        email=user.email,
        password=user.password,
        role=user.role  # Added role field
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
    # Check if user exists with given email or phone
    user = db.query(models.User).filter(
        or_(
            models.User.email == identifier,
            models.User.phone == identifier
        )
    ).first()
    
    if not user:
        return None
    
    # Verify password and role
    if user.password == password and user.role == role:
        return user
    
    return None

def get_user_appointments(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    """
    Get appointments for a specific user
    """
    return db.query(models.Appointment)\
             .filter(models.Appointment.patient_name == db.query(models.User)\
             .filter(models.User.id == user_id).first().name)\
             .offset(skip).limit(limit).all()

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    """
    Create a new appointment
    """
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    try:
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        db.rollback()
        raise e

def update_user_password(db: Session, user_id: int, new_password: str):
    """
    Update user password
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if user:
        user.password = new_password  # In production, hash this password
        try:
            db.commit()
            return True
        except Exception as e:
            db.rollback()
            raise e
    return False