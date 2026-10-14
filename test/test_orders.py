import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)


def test_create_order_success():
    """
    Verify that posting a valid order payload returns 201
    and the response body contains the submitted item, quantity, and a generated id.
    """
    payload = {"item": "burger", "quantity": 2}
    response = client.post("/orders", json=payload)
    assert response.status_code == 201
    data = response.json()
    assert data["item"] == "burger"
    assert data["quantity"] == 2
    assert "id" in data


def test_create_order_missing_fields():
    """
    Verify that posting an empty payload triggers a 422 Unprocessable Entity,
    meaning FastAPI's request validation is working correctly.
    """
    response = client.post("/orders", json={})
    assert response.status_code == 422


def test_get_order_by_id():
    """
    Verify that an order can be retrieved by its id after creation.
    Creates an order first, then fetches it and confirms the id matches.
    """
    create = client.post("/orders", json={"item": "pizza", "quantity": 1})
    order_id = create.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id


def test_get_order_not_found():
    """
    Verify that requesting an order with a non-existent id returns 404,
    confirming the API handles missing resources correctly.
    """
    response = client.get("/orders/999999")
    assert response.status_code == 404


def test_list_orders_returns_list():
    """
    Verify that the GET /orders endpoint returns a list,
    even if the list is empty.
    """
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_health_check():
    """
    Verify that the /health endpoint responds with 200
    and returns a status of 'ok', indicating the app is running.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


@patch("app.database.get_db")
def test_create_order_db_failure(mock_db):
    """
    Verify that when the database raises an exception during order creation,
    the API responds with 503 Service Unavailable instead of an unhandled crash.
    """
    mock_db.side_effect = Exception("DB connection failed")
    response = client.post("/orders", json={"item": "tacos", "quantity": 3})
    assert response.status_code == 503
