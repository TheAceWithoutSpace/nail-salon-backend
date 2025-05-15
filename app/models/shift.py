from sqlalchemy import Column, Integer, Date, Time, ForeignKey, Boolean
from sqlalchemy.orm import relationship
from app.database import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    worker_id = Column(Integer, ForeignKey("workers.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    booked = Column(Boolean, default=False)

    worker = relationship("Worker", back_populates="shifts")
    user = relationship("User", back_populates="shifts", lazy="joined", uselist=False)
