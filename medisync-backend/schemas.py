from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class UserBase(BaseModel):
    name: str
    phone: str
    email: str

class PatientCreate(UserBase):
    password: str
    age: int
    blood_group: str
    medical_history: str

class DoctorCreate(UserBase):
    password: str
    department: str
    description: str
    image_url: Optional[str] = "https://placehold.co/300x200"

class AdminCreate(UserBase):
    password: str
    department: Optional[str] = None

class UserLogin(BaseModel):
    identifier: str  # Email or phone
    password: str
    user_type: str  # "patient", "doctor", or "admin"

class PatientResponse(UserBase):
    id: int
    age: int
    blood_group: str
    medical_history: str

    class Config:
        from_attributes = True

# Updated DoctorResponse to match frontend requirements
class DoctorResponse(BaseModel):
    id: int
    name: str
    department: str
    description: str
    image_url: Optional[str] = "https://placehold.co/300x200"

    class Config:
        from_attributes = True

class AdminResponse(UserBase):
    id: int
    department: Optional[str]

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    status: str = "pending"

class AppointmentResponse(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    appointment_time: datetime
    status: str
    patient: PatientResponse
    doctor: DoctorResponse

    class Config:
        from_attributes = True

class PatientProfileResponse(BaseModel):
    header: str
    patient_info: dict

    class Config:
        from_attributes = True