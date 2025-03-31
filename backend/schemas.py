from pydantic import BaseModel, EmailStr, constr
from typing import Optional

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

class AppointmentCreate(BaseModel):
    patient_name: str
    time: str
    status: str

class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True

# Optional: Add this if you want to handle token-based authentication later
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None
    role: Optional[str] = None