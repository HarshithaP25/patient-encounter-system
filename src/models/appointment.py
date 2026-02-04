from sqlalchemy import Column, Integer, DateTime, ForeignKey
from datetime import datetime, timezone
from database import Base


class Appointment(Base):
    __tablename__ = "harshitha_appointments"

    id = Column(Integer, primary_key=True)
    patient_id = Column(Integer, ForeignKey("harshitha_patients.id"))
    doctor_id = Column(Integer, ForeignKey("harshitha_doctors.id"))
    start_time = Column(DateTime, nullable=False, index=True)
    duration_minutes = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
