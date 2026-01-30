from datetime import date, datetime, timedelta, timezone

# from typing import List
from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session

from src.database import Base, engine, SessionLocal

# ✅ IMPORT ALL MODELS BEFORE create_all
from src.models.patient import Patient
from src.models.doctor import Doctor
from src.models.appointment import Appointment

from src.schemas.patient import PatientCreate, PatientRead
from src.schemas.doctor import DoctorCreate, DoctorRead
from src.schemas.appointment import AppointmentCreate
from src.services.appointment_service import create_appointment


# ---------------- APP & DB INIT ----------------

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Medical Encounter Management System", version="0.1.0")


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# ---------------- PATIENT APIs ----------------


@app.post("/patients", response_model=PatientRead, status_code=201)
def create_patient(patient: PatientCreate, db: Session = Depends(get_db)):
    obj = Patient(**patient.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/patients/{patient_id}", response_model=PatientRead)
def get_patient(patient_id: int, db: Session = Depends(get_db)):
    patient = db.get(Patient, patient_id)
    if not patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return patient


# ---------------- DOCTOR APIs ----------------


@app.post("/doctors", response_model=DoctorRead, status_code=201)
def create_doctor(doctor: DoctorCreate, db: Session = Depends(get_db)):
    obj = Doctor(**doctor.model_dump())
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj


@app.get("/doctors/{doctor_id}", response_model=DoctorRead)
def get_doctor(doctor_id: int, db: Session = Depends(get_db)):
    doctor = db.get(Doctor, doctor_id)
    if not doctor:
        raise HTTPException(status_code=404, detail="Doctor not found")
    return doctor


# ---------------- APPOINTMENT APIs ----------------


@app.post("/appointments", status_code=201)
def schedule_appointment(data: AppointmentCreate, db: Session = Depends(get_db)):
    try:
        return create_appointment(db, data)
    except ValueError as e:
        raise HTTPException(status_code=409, detail=str(e))


@app.get("/appointments")
def get_appointments(
    date: date,
    doctor_id: int | None = None,
    db: Session = Depends(get_db),
):
    """
    Retrieve all appointments for a given date.
    Optionally filter by doctor_id.
    """

    # Timezone-aware start & end of day (UTC)
    start_of_day = datetime.combine(date, datetime.min.time(), tzinfo=timezone.utc)
    end_of_day = start_of_day + timedelta(days=1)

    query = db.query(Appointment).filter(
        Appointment.start_time >= start_of_day, Appointment.start_time < end_of_day
    )

    if doctor_id is not None:
        query = query.filter(Appointment.doctor_id == doctor_id)

    return query.all()
