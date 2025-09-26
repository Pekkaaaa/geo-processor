"""
Test module for the Geo Processor application.

This module contains the tests for the Geo Processor application.
"""

from fastapi.testclient import TestClient

from app.main import app
from app.config import settings

client = TestClient(app)


def test_missing_api_key():
    r = client.post("/api/process", json={"points": [{"lat": 10, "lng": 20}]})
    assert r.status_code == 401
    assert "error" in r.json()


def test_invalid_api_key():
    r = client.post(
        "/api/process",
        headers={"x-api-key": "wrong"},
        json={"points": [{"lat": 10, "lng": 20}]},
    )
    assert r.status_code == 401


def test_valid_api_key():
    r = client.post(
        "/api/process",
        headers={"x-api-key": settings.api_key},
        json={"points": [{"lat": 10, "lng": 20}, {"lat": 30, "lng": 40}]},
    )
    assert r.status_code == 200
    assert "centroid" in r.json()
