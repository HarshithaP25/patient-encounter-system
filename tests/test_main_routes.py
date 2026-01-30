from fastapi.testclient import TestClient
from datetime import datetime, timedelta, timezone

from src.main import app

client = TestClient(app)


def test_get_patient_not_found():
    response = client.get("/patients/9999")
    assert response.status_code == 404


def test_get_doctor_not_found():
    response = client.get("/doctors/9999")
    assert response.status_code == 404


def test_create_patient():
    response = client.post(
        "/patients",
        json={
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@example.com",
            "phone": "9999999999",
        },
    )
    assert response.status_code == 201
    assert response.json()["email"] == "testuser@example.com"


def test_create_doctor():
    response = client.post(
        "/doctors",
        json={
            "full_name": "Dr Test",
            "specialization": "General",
        },
    )
    assert response.status_code == 201
    assert response.json()["is_active"] is True


def test_create_appointment_invalid_date():
    response = client.post(
        "/appointments",
        json={
            "patient_id": 1,
            "doctor_id": 1,
            "start_time": (datetime.now(timezone.utc) - timedelta(days=1)).isoformat(),
            "duration_minutes": 30,
        },
    )

    # business rule violation
    assert response.status_code == 409


def test_get_appointments_empty():
    response = client.get(
        "/appointments",
        params={"date": "2030-01-01"},
    )
    assert response.status_code == 200
    assert isinstance(response.json(), list)
