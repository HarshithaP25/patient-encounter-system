import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from src.database import Base
from src.models.patient import Patient
from src.models.doctor import Doctor

# In-memory DB for tests (allowed by PDF)
TEST_DATABASE_URL = "sqlite:///:memory:"


@pytest.fixture
def db_session():
    engine = create_engine(TEST_DATABASE_URL)
    TestingSessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(bind=engine)
    session = TestingSessionLocal()

    # --- Seed minimum required data ---
    patient = Patient(
        first_name="Test",
        last_name="Patient",
        email="test.patient@example.com",
        phone="9999999999",
    )

    doctor = Doctor(
        full_name="Dr. Test",
        specialization="General",
        is_active=True,
    )

    session.add_all([patient, doctor])
    session.commit()

    yield session

    session.close()
