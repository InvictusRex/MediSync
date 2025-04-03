from sqlalchemy.orm import Session
from sqlalchemy import or_, func
from typing import Dict, List, Optional
import models

def get_patient_basic_info(db: Session, patient_id: int) -> Optional[Dict]:
    """
    Get patient's basic information for dashboard header
    Returns patient name and ID
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        return None
    
    return {
        "patient_info": {
            "id": patient.id,
            "name": patient.name
        }
    }

def get_recent_medical_history(db: Session, patient_id: int, limit: int = 5) -> List[Dict]:
    """
    Get the 5 most recent appointments for the dashboard's medical history section
    """
    recent_appointments = (
        db.query(models.Appointment, models.Doctor)
        .join(models.Doctor, models.Appointment.doctor_id == models.Doctor.id)
        .filter(models.Appointment.patient_id == patient_id)
        .order_by(models.Appointment.appointment_time.desc())
        .limit(limit)
        .all()
    )

    return [
        {
            "appointment_id": apt.Appointment.id,
            "doctor_name": apt.Doctor.name,
            "department": apt.Doctor.department,
            "appointment_time": apt.Appointment.appointment_time,
            "status": apt.Appointment.status
        }
        for apt in recent_appointments
    ]

def get_patient_profile(db: Session, patient_id: int) -> Optional[Dict]:
    """
    Get complete patient profile information
    """
    patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if not patient:
        return None
    
    return {
        "profile": {
            "id": patient.id,
            "name": patient.name,
            "age": patient.age,
            "blood_group": patient.blood_group,
            "medical_history": patient.medical_history,
            "phone": patient.phone,
            "email": patient.email
        }
    }

def get_complete_medical_history(db: Session, patient_id: int) -> List[Dict]:
    """
    Get complete appointment history for medical history page
    """
    all_appointments = (
        db.query(models.Appointment, models.Doctor)
        .join(models.Doctor, models.Appointment.doctor_id == models.Doctor.id)
        .filter(models.Appointment.patient_id == patient_id)
        .order_by(models.Appointment.appointment_time.desc())
        .all()
    )

    return [
        {
            "appointment_id": apt.Appointment.id,
            "doctor_name": apt.Doctor.name,
            "department": apt.Doctor.department,
            "appointment_time": apt.Appointment.appointment_time,
            "status": apt.Appointment.status,
            "details": {
                "consultation_notes": getattr(apt.Appointment, 'consultation_notes', None),
                "prescribed_medications": getattr(apt.Appointment, 'prescribed_medications', None),
                "follow_up_required": getattr(apt.Appointment, 'follow_up_required', False)
            }
        }
        for apt in all_appointments
    ]

def format_appointment_details(appointment, doctor) -> Dict:
    """
    Helper function to format appointment details consistently
    """
    return {
        "appointment_id": appointment.id,
        "doctor_name": doctor.name,
        "department": doctor.department,
        "appointment_time": appointment.appointment_time,
        "status": appointment.status
    }