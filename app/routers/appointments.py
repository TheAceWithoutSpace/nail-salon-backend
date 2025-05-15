from datetime import time, date

from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from typing import List

from app import schemas
from app.database import get_db
from app.crud import appointments as crud

router = APIRouter(prefix="/appointments", tags=["Appointments"])


# Get all appointments
@router.get("/", response_model=List[schemas.AppointmentOut])
def get_appointments(db: Session = Depends(get_db)):
    return crud.get_appointments(db)


# Get appointment by Id
@router.get("/{appointment_id}", response_model=schemas.AppointmentOut)
def get_appointment_by_id(appointment_id: int, db: Session = Depends(get_db)):
    appointment = crud.get_appointment_by_id(db, appointment_id)
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")
    return appointment


# Get appointments by worker
@router.get("/worker/{worker_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_worker(worker_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_by_worker(db, worker_id)


# Get appointments by date
@router.get("/date/{appointment_date}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_date(appointment_date: date, db: Session = Depends(get_db)):
    return crud.get_appointments_by_date(db, appointment_date)


# Get appointments by time
@router.get("/time/{appointment_time}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_time(appointment_time: time, db: Session = Depends(get_db)):
    return crud.get_appointments_by_time(db, appointment_time)


# Get appointments by service
@router.get("/service/{service_id}", response_model=List[schemas.AppointmentOut])
def get_appointments_by_service(service_id: int, db: Session = Depends(get_db)):
    return crud.get_appointments_by_service(db, service_id)


# Create a new appointment
@router.post("/", response_model=schemas.AppointmentOut, status_code=status.HTTP_201_CREATED)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db), user_id: int = 1):
    return crud.create_appointment(db, appointment, user_id)


# Modify an existing appointment
@router.put("/{appointment_id}", response_model=schemas.AppointmentOut)
def modify_appointment(appointment_id: int, appointment_update: schemas.AppointmentUpdate,
                       db: Session = Depends(get_db)):
    return crud.modify_appointment(db, appointment_id, appointment_update)


# Delete an appointment
@router.delete("/{appointment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    crud.delete_appointment(db, appointment_id)
    return
