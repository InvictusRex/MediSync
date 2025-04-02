from sqlalchemy.orm import Session
import models
import schemas

def get_user_appointments(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Appointment)\
             .filter(models.Appointment.patient_name == db.query(models.User)\
             .filter(models.User.id == user_id).first().name)\
             .offset(skip).limit(limit).all()

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
