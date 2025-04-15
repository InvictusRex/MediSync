# MediSync - Hospital Management System

![License](https://img.shields.io/badge/license-MIT-blue.svg)
![Python Version](https://img.shields.io/badge/python-3.8+-blue.svg)
![FastAPI](https://img.shields.io/badge/FastAPI-0.68+-green.svg)

MediSync HMS is a modern, full-stack healthcare management system designed to streamline hospital operations and enhance patient care coordination. The system provides real-time monitoring of hospital resources and seamless management of healthcare services. Built with pure HTML, CSS, and JavaScript, it provides an intuitive interface for managing healthcare services without external dependencies.

## ⭐ Key Features

### ✅ Authentication System
- Secure user registration and login
- Role-based access control (Admin, Doctors, Staff)
- JWT token-based authentication

### 📊 Role-Based Dashboards
- **Admin Dashboard** – Manage doctors, patients, and appointments.
- **Doctor Dashboard** – View schedules, manage appointments, and update availability.
- **Patient Dashboard** – Book appointments, view doctor details, and manage health records.

### 📋 Doctor Listings & Appointments
- Patients can browse a **list of available doctors** based on specialization.
- **Timely appointment booking** – Patients select their preferred time slots.
- Doctors can **approve/reject** appointments.

### 🏥 Special Facilities Management
- **Diagnostic Center** (12 Advanced Labs)
- **24/7 Pharmacy Services**
- **15 Specialized Outpatient Clinics**
- **Emergency Services**

## 🔧 Tech Stack

### Backend
- **Python 3.8+**
- **FastAPI** (Asynchronous API framework)
- **SQLAlchemy** (Database ORM)
- **Alembic** (Database Migrations)
- **Pydantic** (Data Validation)

### Frontend
- **HTML5**
- **CSS3** (Custom Responsive Design)
- **Vanilla JavaScript**
- **Dynamic Theme Switching** (Light/Dark mode)

### Database
- **PostgreSQL / MySQL / SQLite** (Configurable based on environment)

## 🧩 Prerequisites
- Python 3.8 or higher
- **pip** (Python package manager)
- **Virtual environment** (Recommended for dependency isolation)
- **PostgreSQL / MySQL** (For production use)

## 🚀 Installation Guide

### 🔹 Clone the Repository
```bash
git clone https://github.com/InvictusRex/MediSync.git
cd MediSync
```

### 🔹 Set Up Virtual Environment
```bash
python -m venv venv
source venv/bin/activate   # On macOS/Linux
venv\Scripts\activate     # On Windows
```

### 🔹 Install Dependencies
```bash
pip install -r requirements.txt
```

### 🔹 Configure Environment Variables
Create a **.env** file and define the required settings:
```env
DATABASE_URL=postgresql://user:password@localhost:5432/medisync
SECRET_KEY=your_secret_key
DEBUG=True
```

### 🔹 Apply Database Migrations
```bash
alembic upgrade head
```

### 🔹 Run the Server
```bash
uvicorn main:app --reload
or
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```
- The API will be available at **http://0.0.0.0:8000**

## 📡 API Endpoints
| Method | Endpoint | Description |
|--------|---------|-------------|
| **POST** | `/auth/register` | Register a new user |
| **POST** | `/auth/login` | Authenticate user |
| **GET** | `/hospitals/resources` | Fetch real-time hospital resources |
| **GET** | `/doctors/list` | Get list of available doctors |

## 🖥️ Running the Frontend
The frontend is built using HTML, CSS, and JavaScript.
1. Open `index.html` in a browser.
2. Modify `config.js` to set API endpoints if necessary.
3. Ensure CORS is enabled for API access.
