from sqlalchemy import Column, Integer, String, Boolean, DateTime
from datetime import datetime, timezone
from src.database import Base


class Doctor(Base):
    __tablename__ = "harshitha_doctors"

    id = Column(Integer, primary_key=True)
    full_name = Column(String(150), nullable=False)
    specialization = Column(String(100))
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
