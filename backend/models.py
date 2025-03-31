from sqlalchemy import Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

DATABASE_URL = "mysql+mysqlconnector://TheKingslayer:rupankar@localhost/medisync"

Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), unique=True, index=True)
    age = Column(Integer)
    blood_group = Column(String(10))
    medical_history = Column(String(300))
    phone = Column(String(20), unique=True)
    email = Column(String(100), unique=True)
    password = Column(String(100))

class Appointment(Base):
    __tablename__ = "appointments"
    id = Column(Integer, primary_key=True, index=True)
    patient_name = Column(String(100), index=True)  # Specify length for VARCHAR
    time = Column(String(50))  # Specify length for VARCHAR
    status = Column(String(50))  # Specify length for VARCHAR

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)