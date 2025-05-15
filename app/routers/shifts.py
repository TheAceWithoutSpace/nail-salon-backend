from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import date
from app.database import get_db
from app import crud, schemas

router = APIRouter(prefix="/shifts", tags=["Shifts"])


# Route to create shifts (Bulk creation)
@router.post("/", response_model=List[schemas.ShiftResponse])
def create_shifts(data: schemas.BulkShiftCreate, db: Session = Depends(get_db)):
    return crud.create_bulk_shifts(db, data)


# Route to get shifts by day
@router.get("/day/{day}", response_model=List[schemas.ShiftOut])
def get_shifts_by_day(day: date, db: Session = Depends(get_db)):
    shifts = crud.get_shifts_by_day(db, day)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this day")
    return shifts


# Route to update shifts by day
@router.put("/day/{day}", response_model=List[schemas.ShiftOut])
def update_shifts_by_day(
        day: date,
        data: schemas.BulkShiftCreate,
        db: Session = Depends(get_db)
):
    shifts = [
        schemas.ShiftCreate(
            day=day,
            worker_id=data.worker_id,
            start_time=slot.start_time,
            end_time=slot.end_time,
        )
        for slot in data.time_slots
    ]
    updated_shifts = crud.update_shifts_by_day(db, day, shifts)
    if not updated_shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this day to update")
    return updated_shifts


# Route to delete shifts by day
@router.delete("/day/{day}")
def delete_shifts_by_day(day: date, worker_id: int, db: Session = Depends(get_db)):
    deleted = crud.delete_shifts_by_day(db, day, worker_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="No shifts found for this day to delete")
    return {"message": "Shifts deleted successfully"}


# Route to get shifts by month
@router.get("/month/{year}/{month}", response_model=List[schemas.ShiftOut])
def get_shifts_by_month(year: int, month: int, db: Session = Depends(get_db)):
    shifts = crud.get_shifts_by_month(db, year, month)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this month")
    return shifts


# Route to get all shifts
@router.get("/", response_model=List[schemas.ShiftOut])
def get_all_shifts(db: Session = Depends(get_db)):
    return crud.get_all_shifts(db)


# Route to get shifts by worker
@router.get("/worker/{worker_id}", response_model=List[schemas.ShiftOut])
def get_shifts_by_worker(worker_id: int, db: Session = Depends(get_db)):
    shifts = crud.get_shifts_by_worker(db, worker_id)
    if not shifts:
        raise HTTPException(status_code=404, detail="No shifts found for this worker")
    return shifts
