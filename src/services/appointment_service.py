from datetime import datetime, timezone, timedelta
from sqlalchemy.orm import Session

from src.models.appointment import Appointment
from src.models.doctor import Doctor


def create_appointment(db: Session, data):
    # --- Timezone validation ---
    if data.start_time.tzinfo is None:
        raise ValueError("Datetime must be timezone-aware")

    if data.start_time <= datetime.now(timezone.utc):
        raise ValueError("Appointment must be in the future")

    # --- Doctor active check ---
    doctor = db.get(Doctor, data.doctor_id)
    if not doctor or not doctor.is_active:
        raise ValueError("Doctor is inactive or does not exist")

    # Normalize incoming time
    new_start = data.start_time.astimezone(timezone.utc)
    new_end = new_start + timedelta(minutes=data.duration_minutes)

    # --- Overlap detection (SQLite + MySQL safe) ---
    existing_appointments = (
        db.query(Appointment).filter(Appointment.doctor_id == data.doctor_id).all()
    )

    for appt in existing_appointments:
        existing_start = appt.start_time

        # 🔧 FIX: normalize DB datetime (SQLite returns naive)
        if existing_start.tzinfo is None:
            existing_start = existing_start.replace(tzinfo=timezone.utc)

        existing_end = existing_start + timedelta(minutes=appt.duration_minutes)

        if existing_start < new_end and existing_end > new_start:
            raise ValueError("Doctor has overlapping appointment")

    appointment = Appointment(**data.model_dump())
    db.add(appointment)
    db.commit()
    db.refresh(appointment)
    return appointment
