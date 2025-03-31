from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    age: int
    blood_group: str
    medical_history: str
    phone: str
    email: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str

class AppointmentCreate(BaseModel):
    patient_name: str
    time: str
    status: str

class AppointmentResponse(AppointmentCreate):
    id: int

    class Config:
        from_attributes = True
