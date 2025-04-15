from sqlalchemy.orm import Session
from models import Appointment, Patient, Doctor
from schemas import AppointmentCreate, AppointmentUpdate, AdminAppointmentResponse
from fastapi import HTTPException
from typing import List, Optional

def get_all_appointments(db: Session) -> List[dict]:
    """Get all appointments with patient and doctor details"""
    appointments = (
        db.query(
            Appointment,
            Patient.name.label("patient_name"),
            Doctor.name.label("doctor_name")
        )
        .join(Patient, Appointment.patient_id == Patient.id)
        .join(Doctor, Appointment.doctor_id == Doctor.id)
        .all()
    )

    return [
        {
            "id": appointment.Appointment.id,
            "appointment_id": f"A{str(appointment.Appointment.id).zfill(6)}",
            "appointment_time": appointment.Appointment.appointment_time.strftime("%Y-%m-%d %H:%M"),  # Convert datetime to string
            "patient_id": f"P{str(appointment.Appointment.patient_id).zfill(6)}",
            "patient_name": appointment.patient_name,
            "doctor_name": appointment.doctor_name,
            "status": appointment.Appointment.status
        }
        for appointment in appointments
    ]

def create_appointment(db: Session, appointment: AppointmentCreate) -> dict:
    """Create a new appointment"""
    try:
        db_appointment = Appointment(
            patient_id=appointment.patient_id,
            doctor_id=appointment.doctor_id,
            appointment_time=appointment.appointment_time,  # Already in string format
            status=appointment.status
        )
        
        db.add(db_appointment)
        db.commit()
        db.refresh(db_appointment)
        
        # Get the complete appointment details including patient and doctor names
        result = (
            db.query(
                Appointment,
                Patient.name.label("patient_name"),
                Doctor.name.label("doctor_name")
            )
            .join(Patient, Appointment.patient_id == Patient.id)
            .join(Doctor, Appointment.doctor_id == Doctor.id)
            .filter(Appointment.id == db_appointment.id)
            .first()
        )
        
        if not result:
            raise HTTPException(status_code=404, detail="Appointment creation failed")
        
        return {
            "id": result.Appointment.id,
            "appointment_id": f"A{str(result.Appointment.id).zfill(6)}",
            "appointment_time": result.Appointment.appointment_time,  # Already in string format
            "patient_id": f"P{str(result.Appointment.patient_id).zfill(6)}",
            "patient_name": result.patient_name,
            "doctor_name": result.doctor_name,
            "status": result.Appointment.status
        }
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def edit_appointment(db: Session, appointment_id: int, appointment_data: AppointmentUpdate) -> Optional[dict]:
    """Update appointment details"""
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if appointment:
        try:
            update_data = appointment_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                if value is not None:  # Only update non-None values
                    setattr(appointment, key, value)
            db.commit()
            db.refresh(appointment)
            
            # Get the complete updated appointment details
            result = (
                db.query(
                    Appointment,
                    Patient.name.label("patient_name"),
                    Doctor.name.label("doctor_name")
                )
                .join(Patient, Appointment.patient_id == Patient.id)
                .join(Doctor, Appointment.doctor_id == Doctor.id)
                .filter(Appointment.id == appointment_id)
                .first()
            )
            
            return {
                "id": result.Appointment.id,
                "appointment_id": f"A{str(result.Appointment.id).zfill(6)}",
                "appointment_time": result.Appointment.appointment_time.strftime("%Y-%m-%d %H:%M"),  # Convert to string
                "patient_id": f"P{str(result.Appointment.patient_id).zfill(6)}",
                "patient_name": result.patient_name,
                "doctor_name": result.doctor_name,
                "status": result.Appointment.status
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return None