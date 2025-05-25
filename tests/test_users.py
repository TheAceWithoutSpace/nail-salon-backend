import random
import uuid

import pytest
from fastapi.testclient import TestClient
from app.main import app  # assuming your FastAPI app is in app.main
from app import schemas
from app.utils.message_sender import format_israeli_number

client = TestClient(app)


@pytest.fixture
def user_data():
    email = f"johndoe_{uuid.uuid4().hex[:6]}@example.com"
    phone_number = f"10000000{random.randint(100, 999)}"
    return {
        "first_name": "John",  # first_name field is required
        "last_name": "Doe",  # last_name field is required
        "phone_number": phone_number,  # Ensure this is a string
        "email": email,  # email is optional, but provide it for completeness
        "birthdate": "1990-01-01",  # birthdate should be in YYYY-MM-DD format
        # user_type is optional; if omitted, it defaults to "customer"
    }


@pytest.fixture
def existing_user(user_data):
    # Create a user via the POST API
    response = client.post("/users/", json=user_data)
    return response.json()  # return the created user


def test_create_user(client, user_data):
    response = client.post("/users/", json=user_data)
    assert response.status_code == 200  # Expect 200 status for successful creation
    assert "id" in response.json()  # Check that a user ID is returned in the response
    assert response.json()["first_name"] == user_data["first_name"]
    assert response.json()["last_name"] == user_data["last_name"]
    assert response.json()["phone_number"] == format_israeli_number(user_data["phone_number"])
    assert response.json()["email"] == user_data["email"]
    assert response.json()["birthdate"] == user_data["birthdate"]


def test_get_user_by_id(existing_user):
    user_id = existing_user["id"]
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id
    assert response.json()["first_name"] == existing_user["first_name"]
    assert response.json()["last_name"] == existing_user["last_name"]


def test_get_user_by_phone(existing_user):
    phone_number = existing_user["phone_number"]
    response = client.get(f"/users/phone/{phone_number}")
    assert response.status_code == 200
    assert response.json()["phone_number"] == phone_number


def test_update_user(existing_user):
    user_id = existing_user["id"]
    updated_data = {
        "first_name": "Jane ",
        "last_name": "Doe",
        "phone_number": "0987654321",
        "email": "janedoe@example.com"
    }
    response = client.put(f"/users/{user_id}", json=updated_data)
    assert response.status_code == 200
    assert response.json()["first_name"] == updated_data["first_name"]
    assert response.json()["last_name"] == updated_data["last_name"]
    assert response.json()["phone_number"] == updated_data["phone_number"]
    assert response.json()["email"] == updated_data["email"]


def test_delete_user(existing_user):
    user_id = existing_user["id"]
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200

    # Verify user is deleted
    response = client.get(f"/users/{user_id}")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_not_found():
    # Trying to get a non-existent user
    response = client.get("/users/9999")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"


def test_get_user_by_phone_not_found():
    # Trying to get a user by a non-existent phone number
    response = client.get("/users/phone/0000000000")
    assert response.status_code == 404
    assert response.json()["detail"] == "User not found"
