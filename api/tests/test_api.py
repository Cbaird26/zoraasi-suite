"""Tests for FastAPI endpoints."""

import pytest
from fastapi.testclient import TestClient

# Import app - ensure we're in api/ context
import sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from main import app

client = TestClient(app)


def test_root():
    r = client.get("/")
    assert r.status_code == 200
    data = r.json()
    assert data["name"] == "Zor-El"
    assert "models" in data


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    data = r.json()
    assert "status" in data
    assert "version" in data


def test_models():
    r = client.get("/models")
    assert r.status_code == 200
    data = r.json()
    assert "models" in data
    assert "soul" in data["models"]


def test_invariants():
    r = client.get("/invariants")
    assert r.status_code == 200
    data = r.json()
    assert data["layer"] == "outer"
    assert len(data["invariants"]) >= 5


def test_query_requires_prompt():
    r = client.post("/query", json={"prompt": "", "mode": "single"})
    assert r.status_code == 422  # validation error


def test_query_valid_payload():
    # Without API keys, this may return 503; we're testing the endpoint exists
    r = client.post(
        "/query",
        json={"prompt": "Hello", "mode": "single", "role": "soul"},
    )
    # 200 if keys present, 503 if not, 429 if rate limited
    assert r.status_code in (200, 503, 429)
