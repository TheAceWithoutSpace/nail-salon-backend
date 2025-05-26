from pydantic import BaseModel, EmailStr, ConfigDict
from datetime import date
from enum import Enum


class UserType(str, Enum):
    customer = "customer"
    worker = "worker"
    admin = "admin"


# Schema for creating a user
class UserCreate(BaseModel):
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr | None = None
    birthdate: date
    user_type: UserType = UserType.customer  # default is customer


# Schema for updating a user
class UserUpdate(BaseModel):
    first_name: str | None = None
    last_name: str | None = None
    phone_number: str | None = None
    email: EmailStr | None = None
    birthdate: date | None = None


# Schema for user output (e.g., when sending data back to the client)
class UserOut(BaseModel):
    id: int
    first_name: str
    last_name: str
    phone_number: str
    email: EmailStr | None
    birthdate: date
    user_type: UserType

    model_config = ConfigDict(from_attributes=True)
