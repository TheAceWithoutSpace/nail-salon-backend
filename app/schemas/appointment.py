from typing import Optional

from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime

from app.models.appointment import AppointmentStatus


# Schema for creating an appointment
class AppointmentCreate(BaseModel):
    customer_name: str
    service: str
    time: datetime
    worker_id: int  # The worker assigned to the appointment
    user_request: str  # Special request from the user for the worker


# Schema for returning appointment details
class Appointment(BaseModel):
    id: int
    user_id: int
    service: str
    appointment_time: datetime
    worker_id: int  # Associated worker for the appointment
    user_request: str  # Special request from the user

    model_config = ConfigDict(from_attributes=True)


# Schema for the output appointment data
class AppointmentOut(BaseModel):
    id: int
    customer_name: str
    service: str
    date_time: datetime = Field(..., alias="appointment_time")
    status: AppointmentStatus  # Added the status field for appointment status
    worker_id: int  # Associated worker for the appointment
    user_request: str  # Special request from the user

    model_config = ConfigDict(from_attributes=True)


# Schema for updating an appointment
class AppointmentUpdate(BaseModel):
    service: Optional[str] = None  # Optional for updates
    appointment_time: Optional[datetime] = None  # Optional, can be updated
    status: AppointmentStatus  # Optional, for updating the status
    worker_id: Optional[int] = None  # Optional, for updating the assigned worker
    user_request: Optional[str] = None  # Optional, user request field

    model_config = ConfigDict(from_attributes=True)


class AppointmentStatusUpdate(BaseModel):
    status: AppointmentStatus
