from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timedelta
from app.database import Base


class VerifyCode(Base):
    __tablename__ = "verify_codes"

    id = Column(Integer, primary_key=True)
    phone_number = Column(String, nullable=False)
    code = Column(String, nullable=False)
    expires_at = Column(DateTime, default=lambda: datetime.utcnow() + timedelta(minutes=5))

