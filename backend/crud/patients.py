from sqlalchemy.orm import Session
from sqlalchemy import or_
import models
import schemas

def get_patient_by_email(db: Session, email: str):
    return db.query(models.Patient).filter(models.Patient.email == email).first()

def get_patient_by_phone(db: Session, phone: str):
    return db.query(models.Patient).filter(models.Patient.phone == phone).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    try:
        db.commit()
        db.refresh(db_patient)
        return db_patient
    except Exception as e:
        db.rollback()
        raise e

def verify_patient(db: Session, identifier: str, password: str):
    patient = db.query(models.Patient).filter(
        or_(
            models.Patient.email == identifier,
            models.Patient.phone == identifier
        )
    ).first()
    
    if patient and patient.verify_password(password):
        return patient
    return None