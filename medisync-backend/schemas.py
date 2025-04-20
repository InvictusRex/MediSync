from pydantic import BaseModel, Field
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

class DoctorUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    department: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None

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

class MedicalHistoryAppointmentResponse(BaseModel):
    appointment_id: int
    date_time: str
    doctor: str
    status: str

    class Config:
        from_attributes = True

class MedicalHistoryResponse(BaseModel):
    name: str
    patient_id: str
    appointments: List[dict]  # List of appointment dictionaries

    class Config:
        from_attributes = True

class DashboardAppointmentResponse(BaseModel):
    appointment_id: int
    date_time: str
    doctor: str
    status: str

    class Config:
        from_attributes = True

class DashboardResponse(BaseModel):
    name: str
    patient_id: str
    recent_appointments: List[dict]  # List of recent appointment dictionaries

    class Config:
        from_attributes = True

class AdminHeaderResponse(BaseModel):
    name: str
    admin_id: str

    class Config:
        from_attributes = True

# Add this new schema for admin dashboard
class AdminDoctorResponse(BaseModel):
    doctor_id: str
    name: str
    department: str
    description: str
    email: str
    phone: str
    image_url: Optional[str] = "https://placehold.co/300x200"

    class Config:
        from_attributes = True

# Add this new schema for admin patient management
class AdminPatientResponse(BaseModel):
    patient_id: str
    name: str
    age: int
    blood_group: str
    email: str
    phone: str
    medical_history: str

    class Config:
        from_attributes = True

# Add this for patient updates (similar to DoctorUpdate)
class PatientUpdate(BaseModel):
    name: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    medical_history: Optional[str] = None
    password: Optional[str] = None

    class Config:
        from_attributes = True

class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    appointment_time: str  # Keep as string in "YYYY-MM-DD HH:MM" format
    status: str = "pending"

    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    appointment_time: Optional[str] = None
    status: Optional[str] = None

    class Config:
        from_attributes = True

class AdminAppointmentResponse(BaseModel):
    id: int
    appointment_id: str
    appointment_time: str
    patient_id: str
    patient_name: str
    doctor_name: str
    status: str

    class Config:
        from_attributes = True

# Add this with your other schemas
class DoctorHeaderResponse(BaseModel):
    name: str
    doctor_id: str
    department: str

    class Config:
        from_attributes = True

class DoctorDashboardAppointment(BaseModel):
    appointment_id: str
    date_time: str
    patient_id: str
    patient_name: str
    status: str

    class Config:
        from_attributes = True

class DoctorDashboardResponse(BaseModel):
    appointments: List[DoctorDashboardAppointment]

    class Config:
        from_attributes = True

class DoctorProfileResponse(BaseModel):
    header: str
    doctor_info: dict

    class Config:
        from_attributes = True

class DoctorAllAppointmentsResponse(BaseModel):
    appointments: List[dict]

    class Config:
        from_attributes = True