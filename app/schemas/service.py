from pydantic import BaseModel, ConfigDict
from typing import List


# Schema for creating a new service
class ServiceCreate(BaseModel):
    name: str
    price: float
    duration: int  # Duration in minutes
    description: str


# Schema for returning service details (including the ID)
class ServiceOut(BaseModel):
    id: int
    name: str
    price: float
    duration: int  # Duration in minutes
    description: str

    model_config = ConfigDict(from_attributes=True)
