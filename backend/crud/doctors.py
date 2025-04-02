from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    try:
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        db.rollback()
        raise e

def get_doctors(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.Doctor).offset(skip).limit(limit).all()

def get_doctor(db: Session, doctor_id: int):
    return db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()

def get_doctors_by_department(db: Session, department: str):
    return db.query(models.Doctor).filter(models.Doctor.department == department).all()

def search_doctors(db: Session, search_term: str):
    return db.query(models.Doctor).filter(
        or_(
            models.Doctor.name.ilike(f"%{search_term}%"),
            models.Doctor.department.ilike(f"%{search_term}%"),
            models.Doctor.description.ilike(f"%{search_term}%")
        )
    ).all()

def get_all_departments(db: Session):
    departments = db.query(models.Doctor.department).distinct().all()
    return [dept[0] for dept in departments]
