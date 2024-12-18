import pytest
from datetime import datetime, timezone


def test_create_transaction(client, test_headers):
    transaction_data = {
        "transaction_id": "test123",
        "user_id": "user001",
        "amount": 100.50,
        "currency": "USD",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    
    response = client.post(
        "/api/v1/transactions", 
        json=transaction_data,
        headers=test_headers
    )
    
    assert response.status_code == 201
    data = response.json()
    assert "message" in data
    assert "task_id" in data
    assert data["message"] == "Transaction received"

def test_delete_transactions(client, test_headers):
    transaction_data = {
        "transaction_id": "test123",
        "user_id": "user001",
        "amount": 100.50,
        "currency": "USD",
        "timestamp": datetime.now(timezone.utc).isoformat()
    }
    client.post(
        "/api/v1/transactions", 
        json=transaction_data,
        headers=test_headers
    )
    
    response = client.delete("/api/v1/transactions", headers=test_headers)
    assert response.status_code == 204
    
    stats_response = client.get("/api/v1/statistics", headers=test_headers)
    stats_data = stats_response.json()
    assert stats_data["total_transactions"] == 0

def test_get_statistics(client, test_headers):
    transactions = [
        {
            "transaction_id": "1",
            "user_id": "user001",
            "amount": 1000.00,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "transaction_id": "2",
            "user_id": "user001",
            "amount": 850.00,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        },
        {
            "transaction_id": "3",
            "user_id": "user001",
            "amount": 500.00,
            "currency": "USD",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    ]
    
    for transaction in transactions:
        client.post(
            "/api/v1/transactions", 
            json=transaction,
            headers=test_headers
        )
    
    response = client.get("/api/v1/statistics", headers=test_headers)
    assert response.status_code == 200
    
    data = response.json()
    assert data["total_transactions"] == 3
    assert data["average_transaction_amount"] == 783.33  # (1000 + 850 + 500) / 3
    assert len(data["top_transactions"]) == 3
    assert data["top_transactions"][0]["amount"] == 1000.00
    assert data["top_transactions"][1]["amount"] == 850.00
    assert data["top_transactions"][2]["amount"] == 500.00

def test_unauthorized_access(client):
    response = client.get("/api/v1/statistics")
    assert response.status_code == 401
    assert "API Key missing" in response.json()["detail"]

def test_invalid_api_key(client):
    headers = {"Authorization": "ApiKey invalid-key"}
    response = client.get("/api/v1/statistics", headers=headers)
    assert response.status_code == 401
    assert "Invalid API Key" in response.json()["detail"]
