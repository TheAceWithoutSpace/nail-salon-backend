from pydantic import BaseModel, ConfigDict
from typing import Optional


class WorkerBase(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: str


class WorkerCreate(WorkerBase):
    pass


class WorkerUpdate(BaseModel):
    first_name: Optional[str]
    last_name: Optional[str]
    phone_number: Optional[str]
    email: Optional[str]


class Worker(WorkerBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
