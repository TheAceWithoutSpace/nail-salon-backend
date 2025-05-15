from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from app.database import Base


class Worker(Base):
    __tablename__ = "workers"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, unique=True)

    appointments = relationship("Appointment", back_populates="worker", cascade="all, delete")

    shifts = relationship("Shift", back_populates="worker", cascade="all, delete-orphan")

