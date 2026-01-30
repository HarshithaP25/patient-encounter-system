from pydantic import BaseModel, Field
from datetime import datetime


class AppointmentCreate(BaseModel):
    patient_id: int
    doctor_id: int
    start_time: datetime
    duration_minutes: int = Field(ge=15, le=180)
