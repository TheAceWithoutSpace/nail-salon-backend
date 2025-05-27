from sqlalchemy import Column, Integer, String, Float
from app.database import Base


class Service(Base):
    __tablename__ = 'services'

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)  # Unique name for the service
    price = Column(Float)  # Price of the service
    description = Column(String)
    duration = Column(Integer)  # Duration in minutes to perform the service
