from fastapi import FastAPI, Depends, HTTPException, Security
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List
import models, schemas
from datetime import datetime
from database import SessionLocal
from crud import patients, doctors, appointments, admins  # Add admins import
from crud import patient_dashboard_header
from crud import patient_profiles  # Change from patient_profile to patient_profiles
from crud import patient_medical_history
from crud import patient_dashboard
from crud import admin_dashboard_header
from crud import admin_dashboard
from crud import admin_doctors 
from crud import admin_patients
from crud import admin_appointments
from schemas import AdminAppointmentResponse, AppointmentCreate, AppointmentUpdate
from crud import doctor_dashboard_header
from crud import doctor_dashboard
from crud import doctor_profiles
from crud import doctor_appointments
from crud import doctor_patients

app = FastAPI()

# CORS middleware configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Security
security = HTTPBearer()


# Database dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Authentication dependency
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Security(security),
    db: Session = Depends(get_db),
):
    try:
        if not credentials:
            raise HTTPException(status_code=401, detail="Invalid authentication")
        return credentials.credentials
    except Exception:
        raise HTTPException(status_code=401, detail="Invalid authentication")


# API endpoints for doctor-list frontend
@app.get("/api/departments", response_model=List[str])
async def get_departments(
    db: Session = Depends(get_db), token: str = Depends(get_current_user)
):
    return doctors.get_all_departments(db)


@app.get("/api/doctors", response_model=List[schemas.DoctorResponse])
async def read_doctors(
    department: Optional[str] = None,
    search: Optional[str] = None,
    db: Session = Depends(get_db),
    token: str = Depends(get_current_user),
):
    if department:
        return doctors.get_doctors_by_department(db, department)
    elif search:
        return doctors.search_doctors(db, search)
    return doctors.get_doctors(db, skip=0, limit=100)


# Your existing endpoints remain unchanged
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
    elif user.user_type == "admin":  # Add admin case
        db_user = admins.verify_admin(
            db, user.identifier, user.password
        )  # You'll need to import admins from crud
    else:
        raise HTTPException(
            status_code=400,
            detail="Invalid user type. Must be 'patient', 'doctor', or 'admin'",
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
            "department": getattr(
                db_user, "department", None
            ),  # Add department for admin/doctor
        },
    }


# Keeping other endpoints but removing duplicates
@app.get("/doctors/{doctor_id}", response_model=schemas.DoctorResponse)
def read_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctors.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# Appointment endpoints remain unchanged
@app.post("/appointments/", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)
):
    return appointments.create_appointment(db, appointment)


@app.get(
    "/patients/{patient_id}/appointments",
    response_model=List[schemas.AppointmentResponse],
)
def read_patient_appointments(
    patient_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return appointments.get_patient_appointments(db, patient_id, skip, limit)


@app.get(
    "/doctors/{doctor_id}/appointments",
    response_model=List[schemas.AppointmentResponse],
)
def read_doctor_appointments(
    doctor_id: int, skip: int = 0, limit: int = 10, db: Session = Depends(get_db)
):
    return appointments.get_doctor_appointments(db, doctor_id, skip, limit)


# Add to your existing endpoints
@app.get("/patient/profile/{username}")
def get_patient_profile(username: str, db: Session = Depends(get_db)):
    patient = patient_profiles.get_patient_profile(
        db, username
    )  # Change to patient_profiles
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient_profiles.format_profile_response(
        patient
    )  # Change to patient_profiles


@app.get("/patient/medical-history/{username}")
def get_medical_history(username: str, db: Session = Depends(get_db)):
    patient = patient_medical_history.get_patient_medical_history_info(db, username)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    appointments = patient_medical_history.get_patient_appointments(db, patient.id)
    return patient_medical_history.format_medical_history_response(
        patient, appointments
    )


@app.get("/patient/dashboard-info/{username}", response_model=schemas.DashboardResponse)
def get_patient_dashboard_info(username: str, db: Session = Depends(get_db)):
    patient = patient_dashboard.get_patient_dashboard_info(db, username)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")

    recent_appointments = patient_dashboard.get_recent_appointments(db, patient.id)
    return patient_dashboard.format_dashboard_response(patient, recent_appointments)


# Admin dashboard header info
@app.get("/admin/dashboard-info/{admin_id}", response_model=schemas.AdminHeaderResponse)
def get_admin_dashboard_info(admin_id: int, db: Session = Depends(get_db)):
    admin = admin_dashboard_header.get_admin_header_info(db, admin_id)
    if not admin:
        raise HTTPException(status_code=404, detail="Admin not found")
    return admin


# Get recent doctors list
@app.get("/admin/recent-doctors")
def get_recent_doctors_endpoint(db: Session = Depends(get_db)):
    return admin_dashboard.get_recent_doctors(db)

# Get all doctors list
@app.get("/admin/doctors-list")
def get_all_doctors_list_endpoint(db: Session = Depends(get_db)):
    return admin_doctors.get_all_doctors_list(db)

@app.get("/admin/doctor/{doctor_id}")
def get_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db)):
    doctor = doctors.get_doctor(db, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# Update doctor information
@app.put("/admin/doctor/{doctor_id}", response_model=schemas.DoctorResponse)
def update_doctor_endpoint(
    doctor_id: int, doctor_data: schemas.DoctorCreate, db: Session = Depends(get_db)
):
    return admin_dashboard.edit_doctor(db, doctor_id, doctor_data)


# Delete doctor
@app.delete("/admin/doctor/{doctor_id}")
def remove_doctor_endpoint(doctor_id: int, db: Session = Depends(get_db)):
    return admin_dashboard.remove_doctor(db, doctor_id)


# Add new doctor
@app.post("/doctors/register", response_model=schemas.DoctorResponse)
def register_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    if doctors.get_doctor_by_email(db, doctor.email):
        raise HTTPException(status_code=400, detail="Email already registered")
    if doctors.get_doctor_by_phone(db, doctor.phone):
        raise HTTPException(status_code=400, detail="Phone number already registered")
    return doctors.create_doctor(db, doctor)

# Get all patients list
@app.get("/admin/patients-list")
def get_all_patients_list_endpoint(db: Session = Depends(get_db)):
    return admin_patients.get_all_patients_list(db)

# Get specific patient details
@app.get("/admin/patient/{patient_id}")
def get_patient_endpoint(patient_id: int, db: Session = Depends(get_db)):
    patient = admin_patients.get_patient_by_id(db, patient_id)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Update patient details
@app.put("/admin/patient/{patient_id}", response_model=schemas.PatientResponse)
def update_patient_endpoint(
    patient_id: int, patient_data: schemas.PatientCreate, db: Session = Depends(get_db)
):
    patient = admin_patients.edit_patient(db, patient_id, patient_data)
    if patient is None:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient

# Remove patient
@app.delete("/admin/patient/{patient_id}")
def remove_patient_endpoint(patient_id: int, db: Session = Depends(get_db)):
    result = admin_patients.remove_patient(db, patient_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/admin/appointments-list", response_model=List[AdminAppointmentResponse])
def get_all_appointments_endpoint(db: Session = Depends(get_db)):
    return admin_appointments.get_all_appointments(db)

@app.get("/admin/appointment/{appointment_id}", response_model=AdminAppointmentResponse)
def get_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    appointment = admin_appointments.get_appointment_by_id(db, appointment_id)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.post("/admin/appointment")
def create_appointment_endpoint(appointment: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return admin_appointments.create_appointment(db, appointment)
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))

@app.put("/admin/appointment/{appointment_id}", response_model=AdminAppointmentResponse)
def update_appointment_endpoint(
    appointment_id: int, appointment_data: AppointmentUpdate, db: Session = Depends(get_db)
):
    appointment = admin_appointments.edit_appointment(db, appointment_id, appointment_data)
    if appointment is None:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment

@app.delete("/admin/appointment/{appointment_id}")
def remove_appointment_endpoint(appointment_id: int, db: Session = Depends(get_db)):
    result = admin_appointments.remove_appointment(db, appointment_id)
    if "error" in result:
        raise HTTPException(status_code=404, detail=result["error"])
    return result

@app.get("/admin/available-doctors/{appointment_time}")
def get_available_doctors_endpoint(appointment_time: datetime, db: Session = Depends(get_db)):
    return admin_appointments.get_available_doctors(db, appointment_time)

# Add this with your other endpoints
@app.get("/doctor/dashboard-info/{username}", response_model=schemas.DoctorHeaderResponse)
def get_doctor_dashboard_info(username: str, db: Session = Depends(get_db)):
    doctor = doctor_dashboard_header.get_doctor_dashboard_info(db, username)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor

@app.get("/doctor/appointments/{username}", response_model=schemas.DoctorDashboardResponse)
def get_doctor_appointments(username: str, db: Session = Depends(get_db)):
    doctor = doctor_dashboard.get_doctor_by_name(db, username)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    appointments = doctor_dashboard.get_doctor_appointments(db, doctor.id)
    return doctor_dashboard.format_dashboard_response(appointments)

@app.put("/doctor/appointment/{appointment_id}")
def update_doctor_appointment(
    appointment_id: int, 
    update_data: schemas.AppointmentUpdate, 
    db: Session = Depends(get_db)
):
    try:
        # Convert string datetime to Python datetime if provided
        new_datetime = datetime.strptime(update_data.appointment_time, "%Y-%m-%d %H:%M:%S") if update_data.appointment_time else None
        
        result = doctor_dashboard.update_appointment(
            db, 
            appointment_id, 
            new_datetime=new_datetime,
            new_status=update_data.status
        )
        if not result:
            raise HTTPException(status_code=404, detail="Appointment not found")
        return {"status": "success", "message": "Appointment updated successfully"}
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
    
@app.get("/doctor/profile/{username}")
def get_doctor_profile(username: str, db: Session = Depends(get_db)):
    doctor = doctor_profiles.get_doctor_profile(db, username)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor_profiles.format_profile_response(doctor)

@app.get("/doctor/all-appointments/{username}")
def get_all_doctor_appointments(username: str, db: Session = Depends(get_db)):
    doctor = doctor_appointments.get_doctor_by_name(db, username)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    appointments = doctor_appointments.get_all_doctor_appointments(db, doctor.id)
    return doctor_appointments.format_appointments_response(appointments)

@app.get("/doctor/patients/{username}")
def get_doctor_patients(username: str, db: Session = Depends(get_db)):
    doctor = doctor_patients.get_doctor_by_name(db, username)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    
    patients = doctor_patients.get_doctor_patients(db, doctor.id)
    return doctor_patients.format_patients_response(patients)