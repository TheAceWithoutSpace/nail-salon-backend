from pydantic import BaseModel
from datetime import datetime

class AppointmentCreate(BaseModel):
    customer_name: str
    service: str
    time: datetime

class Appointment(AppointmentCreate):
    id: int
    status: str

    class Config:
        orm_mode = True
