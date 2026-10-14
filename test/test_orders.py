import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
from app.main import app

client = TestClient(app)

def test_create_order_success():
    payload = {"item": "burger", "quantity": 2}
    response = client.post("/orders", json=payload)
    assert response .status_code == 201
    data = response.json()
    assert data["item"] == "burger"
    assert data["quantity"] == 2
    assert "id" in data

def test_create_order_missing_fields():
    response = client.post("/orders", json={})
    assert response.status_code == 422

def test_get_order_by_id():
    create = client.post("/orders", json={"item": "pizza", "quantity": 1})
    order_id = create.json()["id"]

    response = client.get(f"/orders/{order_id}")
    assert response.status_code == 200
    assert response.json()["id"] == order_id

def test_get_order_not_found():
    response = client.get("/orders")
    assert response.status_code == 404

def test_list_orders_returns_list():
    response = client.get("/orders")
    assert response.status_code == 200
    assert isinstance(response.json(), list)

def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"

@patch("app.database.get_db")
def test_create_order_db_failure(mock_db):
    mock_db.side_effect = Exception("DB connection failed")
    response = client.post("/orders", json={"item": "tacos", "quantity": 3})
    assert response.status_code == 503