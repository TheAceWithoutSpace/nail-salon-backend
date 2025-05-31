import enum

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum, Boolean
from sqlalchemy.orm import relationship
from app.database import Base
from datetime import datetime


class AppointmentStatus(enum.Enum):
    BOOKED = "Booked"
    NO_SHOW = "No-Show"
    DONE = "Done"


class Appointment(Base):
    __tablename__ = 'appointments'

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String)
    service = Column(String)
    appointment_time = Column(DateTime)
    worker_id = Column(Integer, ForeignKey("workers.id"))  # Linking to worker's table
    user_request = Column(String)  # User request field
    user_id = Column(Integer, ForeignKey("users.id"))  # Linking to users table
    status = Column(Enum(AppointmentStatus, name="appointment_status"), default=AppointmentStatus.BOOKED,
                    nullable=False)
    reminder_sent = Column(Boolean, default=False)

    worker = relationship("Worker", back_populates="appointments")  # Assuming you have a Worker model
    user = relationship("User", back_populates="appointments")  # Assuming you have a User model
