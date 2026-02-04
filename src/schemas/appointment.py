from datetime import datetime
from pydantic import BaseModel


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int


class AppointmentRead(BaseModel):
    id: int
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int

    class Config:
        from_attributes = True
