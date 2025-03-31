from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.middleware.cors import CORSMiddleware
import models, schemas, crud
from database import SessionLocal

app = FastAPI()

# Add CORS middleware to the application
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.UserResponse)
def register_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # Check if email exists
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    # Check if phone exists
    db_user = crud.get_user_by_phone(db, phone=user.phone)
    if db_user:
        raise HTTPException(status_code=400, detail="Phone number already registered")
    
    try:
        return crud.create_user(db=db, user=user)
    except Exception as e:
        raise HTTPException(status_code=500, detail="Registration failed")

@app.post("/login")
def login_user(user: schemas.UserLogin, db: Session = Depends(get_db)):
    try:
        db_user = crud.verify_user(
            db,
            identifier=user.identifier,
            password=user.password,
            role=user.role
        )
        
        if not db_user:
            raise HTTPException(
                status_code=401,
                detail="Invalid login credentials"
            )
        
        return {
            "status": "success",
            "message": "Login successful",
            "user": {
                "id": db_user.id,
                "name": db_user.name,
                "email": db_user.email,
                "role": db_user.role
            }
        }
    except Exception as e:
        raise HTTPException(
            status_code=401,
            detail="Invalid login credentials"
        )

@app.get("/appointments", response_model=list[schemas.AppointmentResponse])
def read_appointments(
    skip: int = 0, 
    limit: int = 10, 
    db: Session = Depends(get_db)
):
    try:
        appointments = db.query(models.Appointment).offset(skip).limit(limit).all()
        return appointments
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch appointments"
        )

@app.post("/appointments", response_model=schemas.AppointmentResponse)
def create_appointment(
    appointment: schemas.AppointmentCreate, 
    db: Session = Depends(get_db)
):
    try:
        return crud.create_appointment(db=db, appointment=appointment)
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to create appointment"
        )

# Optional: Add these helper endpoints if needed
@app.get("/users/me", response_model=schemas.UserResponse)
def read_user_profile(db: Session = Depends(get_db)):
    # This would need authentication middleware to get current user
    pass

@app.get("/users/{user_id}/appointments")
def read_user_appointments(
    user_id: int,
    skip: int = 0,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    try:
        appointments = crud.get_user_appointments(db, user_id, skip, limit)
        return appointments
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail="Failed to fetch user appointments"
        )