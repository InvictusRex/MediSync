from pydantic import BaseModel, EmailStr, constr, validator
from typing import Optional, List
from datetime import datetime
from database import get_formatted_time  # Import the formatting function

# User related schemas
class UserCreate(BaseModel):
    name: str
    age: int
    blood_group: str
    medical_history: str
    phone: str
    email: str
    password: str
    role: str = "patient"  # Default role for new users

class UserLogin(BaseModel):
    identifier: str    # Will handle both email and phone
    password: str
    role: str         # To specify user role during login

class UserProfile(BaseModel):
    id: int
    name: str
    age: int
    blood_group: str
    medical_history: str
    phone: str
    email: str
    role: str
    last_login: Optional[str] = None

    @validator('last_login', pre=True)
    def format_last_login(cls, v):
        if isinstance(v, datetime):
            return get_formatted_time(v)
        return v

    class Config:
        from_attributes = True

class UserResponse(BaseModel):
    id: int
    name: str
    email: str
    role: str
    
    class Config:
        from_attributes = True

# Doctor related schemas
class DoctorBase(BaseModel):
    name: str
    department: str
    description: str
    image_url: str

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    created_at: Optional[str] = None

    @validator('created_at', pre=True)
    def format_created_at(cls, v):
        if isinstance(v, datetime):
            return get_formatted_time(v)
        return v

    class Config:
        from_attributes = True

# Appointment related schemas
class AppointmentCreate(BaseModel):
    patient_name: str
    doctor_name: str
    appointment_date: datetime
    status: str = "scheduled"  # Default status

class AppointmentResponse(BaseModel):
    id: int
    patient_name: str
    doctor_name: str
    appointment_date: str
    status: str
    created_at: Optional[str] = None

    @validator('appointment_date', 'created_at', pre=True)
    def format_dates(cls, v):
        if isinstance(v, datetime):
            return get_formatted_time(v)
        return v

    class Config:
        from_attributes = True

# Dashboard related schemas
class AppointmentInfo(BaseModel):
    id: int
    doctor_name: str
    date: str
    status: str

class DashboardSystemInfo(BaseModel):
    timestamp: str
    user_login: str

    @validator('timestamp', pre=True)
    def format_timestamp(cls, v):
        if isinstance(v, datetime):
            return get_formatted_time(v)
        return v

    class Config:
        from_attributes = True

class PatientDashboard(BaseModel):
    system_info: DashboardSystemInfo
    profile: UserProfile
    appointments: List[AppointmentInfo]

    class Config:
        from_attributes = True

# Token-based authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Department list schema
class DepartmentList(BaseModel):
    departments: List[str]

# Update schemas
class UserUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    blood_group: Optional[str] = None
    medical_history: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    
    class Config:
        from_attributes = True

class AppointmentUpdate(BaseModel):
    status: Optional[str] = None
    appointment_date: Optional[datetime] = None

    class Config:
        from_attributes = True