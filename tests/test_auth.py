import pytest
from fastapi.testclient import TestClient
from app.main import app
from app import models, crud, schemas
from unittest.mock import patch
from app.database import SessionLocal

client = TestClient(app)


# Test: Send login code
def test_send_login_code(db_session):
    # Prepare request data
    request_data = {"phone_number": "1234567890"}

    # Patch the CRUD function to mock sending login code
    with patch("app.crud.send_login_code") as mock_send_code:
        mock_send_code.return_value = {"message": "Login code sent successfully"}

        response = client.post("/auth/send-login-code", json=request_data)

        # Assert successful response
        assert response.status_code == 200
        assert response.json() == {"message": "Login code sent successfully"}


# Test: Verify login code - valid case
def test_verify_login_code_valid(db_session):
    phone_number = "1234567890"
    code = "1234"  # Assume this code was sent previously in the send-login-code request

    # Mock the CRUD function to return a valid user
    user = models.User(id=1, phone_number=phone_number)
    with patch("app.crud.verify_login_code") as mock_verify_code:
        mock_verify_code.return_value = user

        response = client.post("/auth/verify-login-code", json={"phone_number": phone_number, "code": code})

        # Assert successful response with a JWT token
        assert response.status_code == 200
        assert "access_token" in response.json()
        assert response.json()["token_type"] == "bearer"


# Test: Verify login code - invalid code
def test_verify_login_code_invalid(db_session):
    phone_number = "1234567890"
    code = "wrong_code"

    # Mock the CRUD function to return None (invalid code)
    with patch("app.crud.verify_login_code") as mock_verify_code:
        mock_verify_code.return_value = None

        response = client.post("/auth/verify-login-code", json={"phone_number": phone_number, "code": code})

        # Assert unauthorized (401) response
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid or expired code"}


# Test: Verify login code - missing phone number
def test_verify_login_code_missing_phone_number():
    response = client.post("/auth/verify-login-code", json={"code": "1234"})

    # Assert bad request (400) for missing phone number
    assert response.status_code == 422
    assert "detail" in response.json()


# Test: Verify login code - missing code
def test_verify_login_code_missing_code():
    response = client.post("/auth/verify-login-code", json={"phone_number": "1234567890"})

    # Assert bad request (400) for missing code
    assert response.status_code == 422
    assert "detail" in response.json()


# Test: Verify login code - expired code (simulate)
def test_verify_login_code_expired(db_session):
    phone_number = "1234567890"
    expired_code = "expired_code"

    # Mock CRUD to simulate expired code
    with patch("app.crud.verify_login_code") as mock_verify_code:
        mock_verify_code.return_value = None  # Simulating expired code or invalid code

        response = client.post("/auth/verify-login-code", json={"phone_number": phone_number, "code": expired_code})

        # Assert unauthorized (401) response
        assert response.status_code == 401
        assert response.json() == {"detail": "Invalid or expired code"}

