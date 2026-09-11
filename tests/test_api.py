"""
Integration tests for FastAPI endpoints: /personalize and /debug/personalization.
"""
import pytest
from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_personalize_endpoint_success():
    payload = {
        "userId": "user_101",
        "question": "Should I consider changing my job in the next few months?"
    }
    response = client.post("/personalize", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert "answer" in data
    assert data["confidence"] in ("HIGH", "MEDIUM", "LOW")
    assert isinstance(data["sourcesUsed"], list)
    assert "Career Horoscope" in data["sourcesUsed"] or "10th House" in data["sourcesUsed"]


def test_debug_personalization_endpoint_success():
    payload = {
        "userId": "user_101",
        "question": "Should I consider changing my job in the next few months?"
    }
    response = client.post("/debug/personalization", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["intent"] == "career"
    assert "Career Horoscope" in data["selectedContext"] or "10th House" in data["selectedContext"]
    assert "Relationship Horoscope" in data["excludedContext"]
    assert data["language"] == "English"
    assert data["tone"] == "Motivational"
    assert "promptMetrics" in data


def test_health_check_endpoint():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"
