from sqlalchemy import Column, Integer, String, Date, Enum
from sqlalchemy.orm import relationship
import enum
from app.database import Base


class UserType(str, enum.Enum):
    customer = "customer"
    worker = "worker"
    admin = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, index=True)
    last_name = Column(String, index=True)
    phone_number = Column(String, unique=True, index=True)
    email = Column(String, nullable=True, unique=True)
    birthdate = Column(Date)
    user_type = Column(Enum(UserType), default=UserType.customer)
    is_verified = Column(Integer, default=0)  # 0 for not verified, 1 for verified

    # Add relationships if needed
    appointments = relationship("Appointment", back_populates="user")
    shifts = relationship("Shift", back_populates="user")
