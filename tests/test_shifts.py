import pytest
from fastapi.testclient import TestClient
from app.main import app
from datetime import date

client = TestClient(app)


@pytest.fixture
def shift_payload(create_worker):
    worker = create_worker()
    return {
        "worker_id": worker.id,
        "day": str(date.today()),
        "time_slots": [
            {"start_time": "09:00", "end_time": "11:00"},
            {"start_time": "12:00", "end_time": "14:00"}
        ]
    }


# ---- CREATE SHIFTS ----
def test_create_shifts(shift_payload):
    response = client.post("/shifts/", json=shift_payload)
    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 2


# ---- GET SHIFTS BY DAY ----
def test_get_shifts_by_day(shift_payload):
    create_response = client.post("/shifts/", json=shift_payload)
    assert create_response.status_code == 200

    day = shift_payload["day"]
    response = client.get(f"/shifts/day/{day}")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---- UPDATE SHIFTS BY DAY ----
def test_update_shifts_by_day(shift_payload):
    # Create initial shifts
    create_response = client.post("/shifts/", json=shift_payload)
    assert create_response.status_code == 200

    # Update with new times
    update_payload = {
        "worker_id": shift_payload["worker_id"],
        "day": shift_payload["day"],
        "time_slots": [
            {"start_time": "10:00", "end_time": "12:00"},
            {"start_time": "13:00", "end_time": "15:00"},
        ]
    }

    response = client.put(
        f"/shifts/day/{update_payload['day']}",
        json=update_payload
    )
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert data[0]["start_time"] == "10:00:00"
    assert data[1]["end_time"] == "15:00:00"


# ---- DELETE SHIFTS BY DAY ----
def test_delete_shifts_by_day(shift_payload):
    # Create initial shifts
    create_response = client.post("/shifts/", json=shift_payload)
    assert create_response.status_code == 200

    day = shift_payload["day"]
    response = client.delete(f"/shifts/day/{day}?worker_id={shift_payload['worker_id']}")
    assert response.status_code == 200
    assert response.json()["message"] == "Shifts deleted successfully"


# ---- GET SHIFTS BY MONTH ----
def test_get_shifts_by_month():
    today = date.today()
    response = client.get(f"/shifts/month/{today.year}/{today.month}")
    assert response.status_code in (200, 404)


# ---- GET ALL SHIFTS ----
def test_get_all_shifts():
    response = client.get("/shifts/")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


# ---- GET SHIFTS BY WORKER ----
def test_get_shifts_by_worker(shift_payload):
    worker_id = shift_payload["worker_id"]
    response = client.get(f"/shifts/worker/{worker_id}")
    assert response.status_code in (200, 404)


# ---- CLEANUP ----
def teardown_module(module):
    app.dependency_overrides = {}
