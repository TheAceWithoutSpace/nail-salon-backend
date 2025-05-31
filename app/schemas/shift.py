from fastapi import Depends
from pydantic import BaseModel, model_validator, ConfigDict
from typing import List, Optional
from datetime import date, time

from app.utils.jwt_auth import get_worker_id_from_token


class ShiftBase(BaseModel):
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_time_order(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class ShiftCreate(ShiftBase):
    day: date
    worker_id: int
    user_id: Optional[int] = None


class ShiftResponse(ShiftBase):
    id: int
    day: date
    worker_id: int = Depends(get_worker_id_from_token)
    user_id: Optional[int]
    booked: bool

    model_config = ConfigDict(from_attributes=True)


class ShiftTimeSlot(BaseModel):
    start_time: time
    end_time: time

    @model_validator(mode="after")
    def check_time_order(self):
        if self.start_time >= self.end_time:
            raise ValueError("start_time must be before end_time")
        return self


class BulkShiftCreate(BaseModel):
    day: date
    time_slots: List[ShiftTimeSlot]
    worker_id: int


class ShiftUpdate(ShiftBase):
    first_name: str | None = None
    last_name: str | None = None


class ShiftOut(ShiftBase):
    id: int
    user_id: Optional[int]  # Assuming there's a foreign key to a user

    model_config = ConfigDict(from_attributes=True)
