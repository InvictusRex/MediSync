from sqlalchemy.orm import Session
from models import Patient, Appointment
from schemas import PatientCreate, PatientResponse, PatientUpdate, AdminPatientResponse
from typing import List, Optional
from fastapi import HTTPException

def get_all_patients_list(db: Session) -> List[dict]:
    """Get all patients for admin view"""
    patients = db.query(Patient).all()
    return [
        {
            "patient_id": f"P{str(patient.id).zfill(6)}",  # Format: P000001
            "name": patient.name,
            "age": patient.age,
            "blood_group": patient.blood_group,
            "email": patient.email,
            "phone": patient.phone,
            "medical_history": patient.medical_history
        }
        for patient in patients
    ]

def get_patient_by_id(db: Session, patient_id: int) -> Optional[dict]:
    """Get specific patient details by ID"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        return {
            "patient_id": f"P{str(patient.id).zfill(6)}",
            "name": patient.name,
            "age": patient.age,
            "blood_group": patient.blood_group,
            "email": patient.email,
            "phone": patient.phone,
            "medical_history": patient.medical_history
        }
    return None

def create_patient(db: Session, patient: PatientCreate) -> dict:
    """Create a new patient"""
    db_patient = Patient(
        name=patient.name,
        email=patient.email,
        phone=patient.phone,
        password=patient.password,  # Note: In production, ensure password is hashed
        age=patient.age,
        blood_group=patient.blood_group,
        medical_history=patient.medical_history
    )
    try:
        db.add(db_patient)
        db.commit()
        db.refresh(db_patient)
        return get_patient_by_id(db, db_patient.id)
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))

def edit_patient(db: Session, patient_id: int, patient_data: PatientUpdate) -> dict:
    """Update patient details"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        try:
            update_data = patient_data.dict(exclude_unset=True)
            for key, value in update_data.items():
                setattr(patient, key, value)
            db.commit()
            db.refresh(patient)
            return {
                "id": patient.id,  # Add this line
                "patient_id": f"P{str(patient.id).zfill(6)}",
                "name": patient.name,
                "age": patient.age,
                "blood_group": patient.blood_group,
                "email": patient.email,
                "phone": patient.phone,
                "medical_history": patient.medical_history
            }
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return None

def remove_patient(db: Session, patient_id: int) -> dict:
    """Remove a patient and their associated appointments"""
    patient = db.query(Patient).filter(Patient.id == patient_id).first()
    if patient:
        try:
            # First, delete associated appointments
            db.query(Appointment).filter(Appointment.patient_id == patient_id).delete()
            # Then delete the patient
            db.delete(patient)
            db.commit()
            return {"message": "Patient and associated appointments removed successfully"}
        except Exception as e:
            db.rollback()
            raise HTTPException(status_code=400, detail=str(e))
    return {"error": "Patient not found"}