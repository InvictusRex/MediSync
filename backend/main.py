from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import models, schemas
from database import SessionLocal
from crud import patients, doctors, appointments, admins, patient_dashboard

app = FastAPI()

# CORS middleware configuration - Allow all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# API endpoints for doctor-list frontend
@app.get("/api/departments", response_model=List[str])
async def get_departments(db: Session = Depends(get_db)):
    return doctors.get_all_departments(db)

@app.get("/api/doctors", response_model=List[schemas.DoctorResponse])
async def read_doctors(
    department: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db)
):
    if department:
        return doctors.get_doctors_by_department(db, department)
    elif search:
        return doctors.search_doctors(db, search)
    return doctors.get_doctors(db, skip=0, limit=100)

# Patient Dashboard endpoints
@app.get("/api/patient-dashboard/{patient_id}", response_model=schemas.PatientDashboardResponse)
async def get_patient_dashboard(patient_id: int, db: Session = Depends(get_db)):
    basic_info = patient_dashboard.get_patient_basic_info(db, patient_id)
    if not basic_info:
        raise HTTPException(status_code=404, detail="Patient not found")
    
    recent_history = patient_dashboard.get_recent_medical_history(db, patient_id)
    return {
        "patient_info": basic_info,
        "recent_appointments": recent_history
    }

@app.get("/api/patient-profile/{patient_id}", response_model=schemas.PatientResponse)
async def get_patient_profile(patient_id: int, db: Session = Depends(get_db)):
    profile = patient_dashboard.get_patient_profile(db, patient_id)
    if not profile:
        raise HTTPException(status_code=404, detail="Patient not found")
    return profile

@app.get("/api/patient-medical-history/{patient_id}", response_model=List[schemas.AppointmentResponse])
async def get_patient_medical_history(patient_id: int, db: Session = Depends(get_db)):
    return patient_dashboard.get_complete_medical_history(db, patient_id)

# Registration endpoints
@app.post("/patients/register", response_model=schemas.PatientResponse)
def register_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    if patients.get_patient_by_email(db, patient.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if patients.get_patient_by_phone(db, patient.phone):
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return patients.create_patient(db, patient)

@app.post("/doctors/register", response_model=schemas.DoctorResponse)
def register_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    if doctors.get_doctor_by_email(db, doctor.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if doctors.get_doctor_by_phone(db, doctor.phone):
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return doctors.create_doctor(db, doctor)

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    if user.user_type == "patient":
        db_user = patients.verify_patient(db, user.identifier, user.password)
    elif user.user_type == "doctor":
        db_user = doctors.verify_doctor(db, user.identifier, user.password)
    elif user.user_type == "admin":
        db_user = admins.verify_admin(db, user.identifier, user.password)
    else:
        raise HTTPException(
            status_code=400, 
            detail="Invalid user type. Must be 'patient', 'doctor', or 'admin'"
        )

    if not db_user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    return {
        "status": "success",
        "message": "Login successful",
        "user": {
            "id": db_user.id,
            "name": db_user.name,
            "email": db_user.email,
            "type": user.user_type,
            "department": getattr(db_user, 'department', None)
        }
    }

@app.get("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctors.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

# Appointment endpoints
@app.post("/appointments/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate,
    db: Session = Depends(get_db)
):
    return appointments.create_appointment(db, appointment)

@app.get("/patients/{patient_id}/appointments", response_model=List[schemas.AppointmentResponse])
def read_patient_appointments(
    patient_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return appointments.get_patient_appointments(db, patient_id, skip, limit)

@app.get("/doctors/{doctor_id}/appointments", response_model=List[schemas.AppointmentResponse])
def read_doctor_appointments(
    doctor_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    return appointments.get_doctor_appointments(db, doctor_id, skip, limit)