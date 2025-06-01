from sqlite3 import Date
from typing import List

from fastapi import HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import case
from app import models, schemas
from datetime import date, time, datetime, timedelta

from app.models import Appointment
from app.models.appointment import AppointmentStatus
from app.schemas.appointment import AppointmentUpdate


# Get all appointments
def get_appointments(db: Session):
    return db.query(models.Appointment).all()


# Get appointments by worker
def get_appointments_by_worker(db: Session, worker_id: int):
    return db.query(models.Appointment).filter(models.Appointment.worker_id == worker_id).all()


# Get appointment by id
def get_appointment_by_id(db: Session, appointment_id: int):
    return db.query(Appointment).filter(Appointment.id == appointment_id).first()


# Get appointments by date
def get_appointments_by_date(db: Session, appointment_date: date):
    start_dt = datetime.combine(appointment_date, time.min)
    end_dt = datetime.combine(appointment_date, time.max)

    return db.query(models.Appointment).filter(
        models.Appointment.appointment_time >= start_dt,
        models.Appointment.appointment_time <= end_dt
    ).all()


# Get appointments by date and worker_id
def get_appointments_by_date_and_worker(db: Session, appointment_date: date, worker_id: int):
    start_dt = datetime.combine(appointment_date, time.min)
    end_dt = datetime.combine(appointment_date, time.max)

    return db.query(models.Appointment).filter(
        models.Appointment.appointment_time >= start_dt,
        models.Appointment.appointment_time <= end_dt,
        models.Appointment.worker_id == worker_id
    ).order_by(
        case(
            (models.Appointment.status == AppointmentStatus.BOOKED, 0),
            (models.Appointment.status == AppointmentStatus.NO_SHOW, 2),
            (models.Appointment.status == AppointmentStatus.DONE, 3),
            else_=1
        ),
        models.Appointment.start_time
    ).all()


# Get appointments by time
def get_appointments_by_time(db: Session, appointment_time: time):
    return db.query(models.Appointment).filter(models.Appointment.time == appointment_time).all()


# Get appointment by user_id
def get_appointments_by_user(db: Session, user_id: int) -> List[Appointment]:
    return db.query(Appointment).filter(Appointment.user_id == user_id).order_by(
        Appointment.appointment_time.desc()).all()


# Get appointments by service
def get_appointments_by_service(db: Session, service_id: int):
    return db.query(models.Appointment).filter(models.Appointment.service_id == service_id).all()


# Create a new appointment
def create_appointment(db: Session, appointment: schemas.AppointmentCreate, user_id: int):
    db_appointment = models.Appointment(
        customer_name=appointment.customer_name,
        service=appointment.service,
        appointment_time=appointment.time,
        worker_id=appointment.worker_id,  # Assigning the worker to the appointment
        user_request=appointment.user_request,  # Saving the user's special request
        user_id=user_id,  # Assuming user_id is being passed or handled elsewhere
        status=AppointmentStatus.BOOKED  # Default status for a new appointment
    )
    db.add(db_appointment)
    db.commit()
    db.refresh(db_appointment)
    return db_appointment


# Modify an existing appointment (service, date, time)
def modify_appointment(db: Session, appointment_id: int, appointment_update: AppointmentUpdate):
    db_appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()

    if db_appointment:
        # Check each field and update only if it's not None
        if appointment_update.service:
            db_appointment.service = appointment_update.service
        if appointment_update.appointment_time:
            db_appointment.appointment_time = appointment_update.appointment_time
        if appointment_update.status:
            db_appointment.status = appointment_update.status
        if appointment_update.worker_id:
            db_appointment.worker_id = appointment_update.worker_id
        if appointment_update.user_request:
            db_appointment.user_request = appointment_update.user_request

        # Commit the changes to the database
        db.commit()
        db.refresh(db_appointment)
        return db_appointment

    return None  # Return None if the appointment was not found


# Delete an appointment
def delete_appointment(db: Session, appointment_id: int):
    db_appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if db_appointment:
        db.delete(db_appointment)
        db.commit()
        return db_appointment
    return None


# update the appointment status
def update_appointment_status(db: Session, appointment_id: int, new_status: AppointmentStatus):
    appointment = db.query(Appointment).filter(Appointment.id == appointment_id).first()
    if not appointment:
        raise HTTPException(status_code=404, detail="Appointment not found")

    appointment.status = new_status
    db.commit()
    db.refresh(appointment)
    return appointment


# get the reminder status for the appointment
def get_appointments_for_reminder(db: Session):
    today = date.today()
    tomorrow = today + timedelta(days=1)

    appointments = db.query(Appointment).filter(
        Appointment.reminder_sent == False,
        Appointment.status == AppointmentStatus.BOOKED,
        Appointment.appointment_time.cast(Date).in_([today, tomorrow])
    ).all()

    return appointments
