from sqlalchemy.orm import Session
import models
import schemas
from datetime import datetime

def create_appointment(db: Session, appointment: schemas.AppointmentCreate):
    db_appointment = models.Appointment(**appointment.dict())
    db.add(db_appointment)
    try:
        db.commit()
        db.refresh(db_appointment)
        return db_appointment
    except Exception as e:
        db.rollback()
        raise e

def get_patient_appointments(db: Session, patient_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment)\
             .filter(models.Appointment.patient_id == patient_id)\
             .offset(skip).limit(limit).all()

def get_doctor_appointments(db: Session, doctor_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment)\
             .filter(models.Appointment.doctor_id == doctor_id)\
             .offset(skip).limit(limit).all()

def get_appointment(db: Session, appointment_id: int):
    return db.query(models.Appointment)\
             .filter(models.Appointment.id == appointment_id).first()

def update_appointment_status(db: Session, appointment_id: int, status: str):
    appointment = get_appointment(db, appointment_id)
    if appointment:
        appointment.status = status
        try:
            db.commit()
            return appointment
        except Exception as e:
            db.rollback()
            raise e
    return None