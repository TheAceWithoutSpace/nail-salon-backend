from typing import List

from sqlalchemy.orm import Session

from app import models
from app.models.shift import Shift
from app.schemas.shift import BulkShiftCreate, ShiftCreate
from datetime import datetime, date, timedelta, time


def create_shifts(db: Session, data: BulkShiftCreate):
    for slot in data.time_slots:
        db.add(Shift(
            day=data.day,
            start_time=slot.start_time,
            end_time=slot.end_time,
            worker_id=data.worker_id,
            booked=False
        ))
    db.commit()


def get_shifts_by_day(db: Session, day: date):
    return db.query(Shift).filter(Shift.day == day).all()


def get_shifts_by_day_and_worker(db: Session, day: date, worker_id: int):
    return (
        db.query(Shift)
        .filter(
            Shift.day == day,
            Shift.worker_id == worker_id
        )
        .all()
    )


def get_shifts_by_month(db: Session, year: int, month: int):
    from datetime import date
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)
    return db.query(Shift).filter(Shift.day >= start, Shift.day < end).all()


def get_shifts_by_month_and_worker(db: Session, year: int, month: int, worker_id: int):
    start = date(year, month, 1)
    end = date(year + 1, 1, 1) if month == 12 else date(year, month + 1, 1)

    return (
        db.query(Shift)
        .filter(
            Shift.worker_id == worker_id,
            Shift.day >= start,
            Shift.day < end
        )
        .all()
    )


def get_all_shifts(db: Session):
    return db.query(Shift).all()


def update_shifts_by_day(db: Session, day: date, data: list[ShiftCreate]):
    worker_id = data[0].worker_id  # Take worker_id from the first shift (if all are same)

    # Delete existing shifts for the specified day and worker
    db.query(Shift).filter(Shift.day == day, Shift.worker_id == worker_id).delete()

    # Add the new shifts
    for shift in data:
        db.add(Shift(
            day=shift.day,
            worker_id=shift.worker_id,
            start_time=shift.start_time,
            end_time=shift.end_time,
        ))

    db.commit()

    updated = db.query(Shift).filter(Shift.day == day, Shift.worker_id == worker_id).all()
    return updated


def delete_shifts_by_day(db: Session, day: date, worker_id: int):
    shift_query = db.query(Shift).filter(Shift.day == day, Shift.worker_id == worker_id)
    if not shift_query.first():
        return None
    shift_query.delete()
    db.commit()
    return {"detail": "Shift deleted"}


def get_shifts_by_worker(db: Session, worker_id: int):
    return db.query(Shift).filter(Shift.worker_id == worker_id).all()


def create_bulk_shifts(db: Session, payload: BulkShiftCreate) -> List[Shift]:
    shifts = []
    for slot in payload.time_slots:
        shift = Shift(
            day=payload.day,
            start_time=slot.start_time.replace(microsecond=0),
            end_time=slot.end_time.replace(microsecond=0),
            worker_id=payload.worker_id,
        )
        db.add(shift)
        shifts.append(shift)
    db.commit()
    return shifts


def get_worker_shift_summary(db: Session, worker_id: int):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    # Start and end of today
    today_start = datetime.combine(today, time.min)  # 00:00:00
    today_end = datetime.combine(today, time.max)  # 23:59:59.999999

    # Start and end of tomorrow
    tomorrow_start = datetime.combine(tomorrow, time.min)
    tomorrow_end = datetime.combine(tomorrow, time.max)
    print(today)
    print(tomorrow)
    today_shifts = db.query(models.Shift).filter(
        models.Shift.worker_id == worker_id,
        models.Shift.day.between(today_start, today_end)
    ).count()

    tomorrow_shifts = db.query(models.Shift).filter(
        models.Shift.worker_id == worker_id,
        models.Shift.day.between(tomorrow_start, tomorrow_end)
    ).count()

    today_appointments = db.query(models.Appointment).filter(
        models.Appointment.worker_id == worker_id,
        models.Appointment.appointment_time.between(today_start, today_end)
    ).count()

    tomorrow_appointments = db.query(models.Appointment).filter(
        models.Appointment.worker_id == worker_id,
        models.Appointment.appointment_time.between(tomorrow_start, tomorrow_end)
    ).count()

    return {
        "today": {
            "shifts": today_shifts,
            "appointments": today_appointments
        },
        "tomorrow": {
            "shifts": tomorrow_shifts,
            "appointments": tomorrow_appointments
        }
    }
