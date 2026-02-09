import pytest
from fastapi.testclient import TestClient
from src.app import app

client = TestClient(app)

def test_get_activities():
    response = client.get("/activities")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, dict)
    assert all('description' in v for v in data.values())

def test_signup_and_prevent_duplicate():
    # Use a test email and activity
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser@example.com"
    # First signup should succeed
    resp1 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp1.status_code == 200
    # Second signup should fail (duplicate)
    resp2 = client.post(f"/activities/{activity}/signup?email={email}")
    assert resp2.status_code == 400
    assert "already signed up" in resp2.json().get("detail", "")

def test_unregister():
    activity = next(iter(client.get("/activities").json().keys()))
    email = "testuser2@example.com"
    # Register first
    client.post(f"/activities/{activity}/signup?email={email}")
    # Unregister
    resp = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp.status_code == 200
    # Unregister again should fail
    resp2 = client.post(f"/activities/{activity}/unregister?email={email}")
    assert resp2.status_code == 400
    assert "not registered" in resp2.json().get("detail", "")
