from sqlalchemy.orm import Session
from sqlalchemy import asc
import models
import schemas
from typing import List
from fastapi import HTTPException


def get_all_doctors_list(db: Session):
    """
    Fetch all doctors from the database.
    Orders by ID in ascending order
    Returns all doctors without any limit
    """
    try:
        doctors = (
            db.query(models.Doctor).order_by(asc(models.Doctor.id)).all()
        )
        list = []
        for doctor in doctors:
            list.append(format_doctor_response(doctor))
        return list
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving doctors: {str(e)}"
        )


def edit_doctor(db: Session, doctor_id: int, doctor_data: schemas.DoctorUpdate):
    """
    Edit an existing doctor's information
    """
    try:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        # Update doctor's information
        update_data = doctor_data.dict(exclude_unset=True)

        # Keep existing description and image_url if not provided
        if "description" not in update_data:
            update_data["description"] = doctor.description
        if "image_url" not in update_data:
            update_data["image_url"] = doctor.image_url

        for key, value in update_data.items():
            setattr(doctor, key, value)

        db.commit()
        db.refresh(doctor)
        return doctor
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error updating doctor: {str(e)}")


def remove_doctor(db: Session, doctor_id: int):
    """
    Remove a doctor from the database
    """
    try:
        doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")

        db.delete(doctor)
        db.commit()
        return {"message": f"Doctor {doctor.name} successfully removed"}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Error removing doctor: {str(e)}")


def format_doctor_id(doctor_id: int) -> str:
    """
    Format doctor ID to display format (e.g., D000001)
    """
    return f"{doctor_id:05d}"


def format_doctor_response(doctor: models.Doctor) -> dict:
    """
    Format doctor data for admin dashboard display
    """
    return {
        "id": format_doctor_id(doctor.id),
        "name": f"Dr. {doctor.name}",
        "department": doctor.department,
        "email": doctor.email,
        "phone": doctor.phone,
        "description": doctor.description,
        "image_url": doctor.image_url,
    }


def get_doctor_by_formatted_id(db: Session, formatted_id: str) -> models.Doctor:
    """
    Get a doctor by their formatted ID (e.g., 'D000123')
    """
    try:
        if not formatted_id.startswith("D") or len(formatted_id) != 7:
            raise HTTPException(status_code=400, detail="Invalid doctor ID format")

        # Extract the numeric part and convert to integer
        numeric_id = int(formatted_id[1:])
        doctor = db.query(models.Doctor).filter(models.Doctor.id == numeric_id).first()

        if not doctor:
            raise HTTPException(status_code=404, detail="Doctor not found")
        return doctor
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid doctor ID format")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error retrieving doctor: {str(e)}"
        )