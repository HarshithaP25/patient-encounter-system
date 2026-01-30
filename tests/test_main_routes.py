from fastapi.testclient import TestClient
from src.main import app

client = TestClient(app)


def test_health_patients_endpoint():
    response = client.get("/patients/9999")
    assert response.status_code in (404, 422)


def test_health_doctors_endpoint():
    response = client.get("/doctors/9999")
    assert response.status_code in (404, 422)
