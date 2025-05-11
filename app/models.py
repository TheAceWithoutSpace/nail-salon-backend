from sqlalchemy import Column, Integer, String, DateTime
from .database import Base

class Appointment(Base):
    __tablename__ = "appointments"

    id = Column(Integer, primary_key=True, index=True)
    customer_name = Column(String, index=True)
    service = Column(String)
    time = Column(DateTime)
    status = Column(String, default="Scheduled")
