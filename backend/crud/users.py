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

def update_user_password(db: Session, user_id: int, new_password: str):
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
