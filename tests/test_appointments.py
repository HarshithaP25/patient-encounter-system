import pytest
from datetime import datetime, timezone, timedelta

from src.schemas.appointment import AppointmentCreate
from src.services.appointment_service import create_appointment
from src.models.doctor import Doctor


# -------------------------------
# TEST 1: Past appointment rejected
# -------------------------------


def test_past_appointment_rejected(db_session):
    data = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) - timedelta(days=1),
        duration_minutes=30,
    )

    with pytest.raises(ValueError, match="future"):
        create_appointment(db_session, data)


# --------------------------------
# TEST 2: Timezone-aware datetime enforced
# --------------------------------


def test_timezone_required(db_session):
    data = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(),  # ❌ naive datetime
        duration_minutes=30,
    )

    with pytest.raises(ValueError, match="timezone"):
        create_appointment(db_session, data)


# --------------------------------
# TEST 3: Overlapping appointment rejected
# --------------------------------


def test_overlapping_appointment_rejected(db_session):
    start_time = datetime.now(timezone.utc) + timedelta(days=1)

    first = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=start_time,
        duration_minutes=60,
    )

    second = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=start_time + timedelta(minutes=30),
        duration_minutes=30,
    )

    create_appointment(db_session, first)

    with pytest.raises(ValueError, match="overlapping"):
        create_appointment(db_session, second)


# --------------------------------
# TEST 4: Inactive doctor cannot be scheduled
# --------------------------------


def test_inactive_doctor_rejected(db_session):
    doctor = db_session.get(Doctor, 1)
    doctor.is_active = False
    db_session.commit()

    data = AppointmentCreate(
        patient_id=1,
        doctor_id=1,
        start_time=datetime.now(timezone.utc) + timedelta(days=1),
        duration_minutes=30,
    )

    with pytest.raises(ValueError, match="inactive"):
        create_appointment(db_session, data)
