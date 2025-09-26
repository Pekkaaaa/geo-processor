"""
Test module for the Geo Processor application.

This module contains the tests for the Geo Processor application.
"""


import pytest
from fastapi.testclient import TestClient

from app.main import app
from app.config import settings

client = TestClient(app)


def test_health():
    r = client.get("/api/health")
    assert r.status_code == 200
    assert r.json().get("success") == True


def test_happy_path():
    payload = {
        "points": [
            {"lat": 40.7128, "lng": -74.0060},   
            {"lat": 34.0522, "lng": -118.2437},  
            {"lat": 41.8781, "lng": -87.6298},  
        ]
    }
    r = client.post("/api/process", headers={"x-api-key": settings.api_key}, json=payload)
    assert r.status_code == 200
    data = r.json()
    assert "centroid" in data and "bounds" in data
    b = data["bounds"]
    assert pytest.approx(b["north"], rel=1e-6) == 41.8781
    assert pytest.approx(b["south"], rel=1e-6) == 34.0522
    assert pytest.approx(b["east"], rel=1e-6) == -74.0060
    assert pytest.approx(b["west"], rel=1e-6) == -118.2437
