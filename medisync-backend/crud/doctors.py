from sqlalchemy.orm import Session
from sqlalchemy import or_, distinct
from fastapi import HTTPException
import models
import schemas
from typing import List

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    try:
        db.commit()
        db.refresh(db_doctor)
        return db_doctor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def get_doctor_by_email(db: Session, email: str):
    return db.query(models.Doctor).filter(models.Doctor.email == email).first()

def get_doctor_by_phone(db: Session, phone: str):
    return db.query(models.Doctor).filter(models.Doctor.phone == phone).first()

def verify_doctor(db: Session, identifier: str, password: str):
    doctor = db.query(models.Doctor).filter(
        or_(
            models.Doctor.email == identifier,
            models.Doctor.phone == identifier
        )
    ).first()
    
    if doctor and doctor.verify_password(password):
        return doctor
    return None

def get_doctors(db: Session, skip: int = 0, limit: int = 100) -> List[models.Doctor]:
    try:
        return db.query(models.Doctor)\
                 .order_by(models.Doctor.name)\
                 .offset(skip)\
                 .limit(limit)\
                 .all()
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error retrieving doctors")

def format_doctor_id(doctor_id: int) -> str:
    """
    Format doctor ID to display format (e.g., D000001)
    """
    return f"D{doctor_id:06d}"

def format_doctor_response(doctor: models.Doctor) -> dict:
    """
    Format doctor data for admin dashboard display
    """
    return {
        "doctor_id": format_doctor_id(doctor.id),
        "name": f"Dr. {doctor.name}",
        "department": doctor.department,
        "email": doctor.email,
        "phone": doctor.phone,
        "description": doctor.description,
        "image_url": doctor.image_url
    }

def get_doctor(db: Session, doctor_id: int):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return format_doctor_response(doctor)

def get_doctors_by_department(db: Session, department: str) -> List[models.Doctor]:
    try:
        return db.query(models.Doctor)\
                 .filter(models.Doctor.department == department)\
                 .order_by(models.Doctor.name)\
                 .all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving doctors for department: {department}"
        )

def search_doctors(db: Session, search_term: str) -> List[models.Doctor]:
    try:
        search_pattern = f"%{search_term}%"
        return db.query(models.Doctor)\
                 .filter(
                     or_(
                         models.Doctor.name.ilike(search_pattern),
                         models.Doctor.department.ilike(search_pattern),
                         models.Doctor.description.ilike(search_pattern)
                     )
                 )\
                 .order_by(models.Doctor.name)\
                 .all()
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error searching for doctors: {search_term}"
        )

def get_all_departments(db: Session) -> List[str]:
    try:
        departments = db.query(distinct(models.Doctor.department))\
                       .filter(models.Doctor.department.isnot(None))\
                       .order_by(models.Doctor.department)\
                       .all()
        return [dept[0] for dept in departments if dept[0]]
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Error retrieving departments"
        )