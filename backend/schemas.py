from pydantic import BaseModel, EmailStr, constr
from typing import Optional

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

    class Config:
        from_attributes = True

# Appointment related schemas
class AppointmentCreate(BaseModel):
    patient_name: str
    time: str
    status: str

class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True

# Optional: Token-based authentication schemas
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None

# Optional: Department list schema (if needed)
class DepartmentList(BaseModel):
    departments: list[str]