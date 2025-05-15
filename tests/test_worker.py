import random
import uuid

import pytest
from fastapi.testclient import TestClient
from app.main import app
from app.models import Worker
from app.database import SessionLocal


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


@pytest.fixture
def create_worker(client):
    def _create_worker(
            first_name="John",
            last_name="Doe",
            phone_number=None,
            email=None,
    ):
        if phone_number is None:
            phone_number = f"10000000{random.randint(100, 999)}"
        if email is None:
            email = f"johndoe_{uuid.uuid4().hex[:6]}@example.com"

        worker_data = {
            "first_name": first_name,
            "last_name": last_name,
            "phone_number": phone_number,
            "email": email,
        }
        response = client.post("/workers/", json=worker_data)
        assert response.status_code == 200, f"Failed to create worker: {response.text}"
        # Return JSON dict, not ORM model
        return response.json()

    return _create_worker


def test_create_worker(client, create_worker):
    worker = create_worker()
    response = client.get(f"/workers/{worker['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == worker["id"]


def test_get_worker(client, create_worker):
    worker = create_worker()
    response = client.get(f"/workers/{worker['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == worker['id']
    assert data["first_name"] == worker['first_name']
    assert data["last_name"] == worker['last_name']
    assert data["phone_number"] == worker['phone_number']
    assert data["email"] == worker['email']


def test_get_workers(client, create_worker):
    create_worker()
    create_worker()
    response = client.get("/workers/")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 1


def test_update_worker(client, create_worker):
    worker = create_worker()
    update_data = {
        "first_name": "Charlie Updated",
        "last_name": "Davis Updated",
        "phone_number": "555765432",
        "email": "charlieupdated@example.com"
    }
    response = client.put(f"/workers/{worker['id']}", json=update_data)
    assert response.status_code == 200
    data = response.json()
    assert data["first_name"] == update_data["first_name"]
    assert data["last_name"] == update_data["last_name"]
    assert data["phone_number"] == update_data["phone_number"]
    assert data["email"] == update_data["email"]


def test_delete_worker(client, create_worker):
    worker = create_worker()
    response = client.delete(f"/workers/{worker['id']}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == worker['id']
    response = client.get(f"/workers/{worker['id']}")
    assert response.status_code == 404
