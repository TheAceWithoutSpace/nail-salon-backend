import uuid

import pytest


# Correct payload matching ServiceCreate schema


def test_create_service(client):
    service_payload = {
        "name": f"Manicure_{uuid.uuid4().hex[:6]}",  # short unique suffix
        "price": 25.0,
        "duration": 60,
        "description": "blop blop"
    }
    response = client.post("/services/", json=service_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == service_payload["name"]
    assert data["price"] == service_payload["price"]
    assert data["duration"] == service_payload["duration"]
    assert data["description"] == service_payload["description"]
    assert "id" in data


def test_get_services(client):
    response = client.get("/services/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    # Optionally, assert that service_payload is in the returned list


def test_get_service_by_id(client):
    service_payload = {
        "name": f"Manicure_{uuid.uuid4().hex[:6]}",  # short unique suffix
        "price": 25.0,
        "duration": 60,
        "description": "blop"
    }
    create_resp = client.post("/services/", json=service_payload)
    service_id = create_resp.json()["id"]

    response = client.get(f"/services/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id
    assert data["name"] == service_payload["name"]
    assert data["duration"] == service_payload["duration"]
    assert data["description"] == service_payload["description"]


def test_get_service_by_id_not_found(client):
    response = client.get("/services/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_update_service(client):
    service_payload = {
        "name": f"Manicure_{uuid.uuid4().hex[:6]}",  # short unique suffix
        "price": 25.0,
        "duration": 60,
        "description": "blop"
    }
    create_resp = client.post("/services/", json=service_payload)
    service_id = create_resp.json()["id"]

    update_payload = {
        "name": "Deluxe Manicure",
        "price": 40.0,
        "duration": 90,
        "description": "this is updated text"
    }
    response = client.put(f"/services/{service_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == update_payload["name"]
    assert data["price"] == update_payload["price"]
    assert data["duration"] == update_payload["duration"]
    assert data["description"] == update_payload["description"]


def test_update_service_not_found(client):
    update_payload = {
        "name": "Non-existent Service",
        "price": 0.0,
        "duration": 30,
        "description": "no service for you "
    }
    response = client.put("/services/999999", json=update_payload)
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"


def test_delete_service(client):
    service_payload = {
        "name": f"Manicure_{uuid.uuid4().hex[:6]}",  # short unique suffix
        "price": 25.0,
        "duration": 60,
        "description": "delete me pls"
    }
    create_resp = client.post("/services/", json=service_payload)
    service_id = create_resp.json()["id"]

    response = client.delete(f"/services/{service_id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == service_id

    # Confirm deletion
    get_resp = client.get(f"/services/{service_id}")
    assert get_resp.status_code == 404


def test_delete_service_not_found(client):
    response = client.delete("/services/999999")
    assert response.status_code == 404
    assert response.json()["detail"] == "Service not found"
