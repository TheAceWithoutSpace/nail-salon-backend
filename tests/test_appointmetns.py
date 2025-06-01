# test_appointments.py
import pytest
from fastapi.testclient import TestClient
from datetime import datetime, timedelta
from app.main import app
from app.models import Appointment, AppointmentStatus

client = TestClient(app)


@pytest.fixture
def create_appointment(db_session, create_worker, create_user):
    def _create():
        worker = create_worker()
        user = create_user()
        appointment = Appointment(
            customer_name="John Doe",
            service="Manicure",
            appointment_time=datetime.utcnow() + timedelta(hours=1),
            worker_id=worker.id,
            user_request="Nail art",
            user_id=user.id,
        )
        db_session.add(appointment)
        db_session.commit()
        db_session.refresh(appointment)
        return appointment

    return _create


def test_create_appointment(client, db_session, create_worker, create_user):
    worker = create_worker()
    user = create_user()
    response = client.post("/appointments/", json={
        "customer_name": "John Doe",
        "service": "Manicure",
        "time": (datetime.utcnow() + timedelta(hours=1)).isoformat(),
        "worker_id": worker.id,
        "user_request": "Nail art",
        "user_id": user.id
    })
    assert response.status_code == 201
    data = response.json()
    assert data["customer_name"] == "John Doe"
    assert data["service"] == "Manicure"


def test_get_appointments(client, create_appointment):
    appointment = create_appointment()
    response = client.get("/appointments/")
    assert response.status_code == 200
    appointments = response.json()
    assert len(appointments) > 0
    assert appointments[0]["customer_name"] == appointment.customer_name


def test_update_appointment(client, db_session, create_appointment, create_worker):
    new_worker = create_worker()
    appointment = create_appointment()
    response = client.put(f"/appointments/{appointment.id}", json={
        "service": "Pedicure",
        "appointment_time": (datetime.utcnow() + timedelta(hours=2)).isoformat(),
        "worker_id": new_worker.id,
        "user_request": "Foot spa",
        "user_id": appointment.user_id,
    })
    assert response.status_code == 200
    updated = response.json()
    assert updated["service"] == "Pedicure"
    assert updated["worker_id"] == new_worker.id


def test_mark_no_show(client, create_appointment):
    appointment = create_appointment()  # Starts as BOOKED

    response = client.patch(f"/appointments/{appointment.id}/mark-no-show")

    assert response.status_code == 200
    data = response.json()
    assert data["appointment_id"] == appointment.id
    assert data["new_status"] == "No-Show"
    assert data["message"] == "Status updated"


def test_mark_done(client, create_appointment):
    appointment = create_appointment()

    response = client.patch(f"/appointments/{appointment.id}/mark-done")

    assert response.status_code == 200
    data = response.json()
    assert data["appointment_id"] == appointment.id
    assert data["new_status"] == "Done"
    assert data["message"] == "Status updated"


def test_mark_booked(client, create_appointment):
    appointment = create_appointment()

    # First, change to NO_SHOW to ensure the status changes
    client.patch(f"/appointments/{appointment.id}/mark-no-show")

    # Then, change back to BOOKED
    response = client.patch(f"/appointments/{appointment.id}/mark-booked")

    assert response.status_code == 200
    data = response.json()
    assert data["appointment_id"] == appointment.id
    assert data["new_status"] == "Booked"
    assert data["message"] == "Status updated"


def test_delete_appointment(client, create_appointment):
    appointment = create_appointment()
    response = client.delete(f"/appointments/{appointment.id}")
    assert response.status_code == 204


def test_get_appointment_by_id(client, create_appointment):
    appointment = create_appointment()
    response = client.get(f"/appointments/{appointment.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == appointment.id
    assert data["customer_name"] == appointment.customer_name
