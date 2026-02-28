"""Tests for Zor-El API endpoints and validation."""
import hashlib
import os

import pytest
from fastapi.testclient import TestClient

from api.main import app, INVARIANTS, API_VERSION, MODELS, SYSTEM_PROMPT


@pytest.fixture
def client():
    with TestClient(app) as c:
        yield c


class TestRootEndpoint:
    def test_root_returns_identity(self, client):
        r = client.get("/")
        assert r.status_code == 200
        data = r.json()
        assert data["name"] == "Zor-El"
        assert data["identity"] == "Zora"
        assert data["layer"] == "outer"
        assert data["version"] == API_VERSION

    def test_root_lists_all_models(self, client):
        r = client.get("/")
        data = r.json()
        for role in MODELS:
            assert role in data["models"]

    def test_root_lists_all_modes(self, client):
        r = client.get("/")
        data = r.json()
        assert "single" in data["modes"]
        assert "router" in data["modes"]
        assert "consensus" in data["modes"]


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        r = client.get("/health")
        assert r.status_code == 200
        data = r.json()
        assert data["version"] == API_VERSION
        assert data["layer"] == "outer"
        assert isinstance(data["models"], list)
        assert len(data["models"]) == len(MODELS)


class TestModelsEndpoint:
    def test_models_returns_all(self, client):
        r = client.get("/models")
        assert r.status_code == 200
        data = r.json()
        assert len(data["models"]) == len(MODELS)
        for role, info in data["models"].items():
            assert "id" in info
            assert "name" in info
            assert "strength" in info


class TestIdentityEndpoint:
    def test_identity_returns_outer_layer(self, client):
        r = client.get("/identity")
        assert r.status_code == 200
        data = r.json()
        assert data["layer"] == "outer"
        assert "Zora" in data["identity"]
        assert len(data["sha256"]) == 64
        assert data["sha256"] == hashlib.sha256(data["identity"].encode()).hexdigest()

    def test_identity_invariants_present(self, client):
        r = client.get("/identity")
        data = r.json()
        assert len(data["invariants"]) == len(INVARIANTS)


class TestInvariantsEndpoint:
    def test_invariants_returns_all(self, client):
        r = client.get("/invariants")
        assert r.status_code == 200
        data = r.json()
        assert data["layer"] == "outer"
        assert len(data["invariants"]) == 5
        ids = [inv["id"] for inv in data["invariants"]]
        assert "zero-purge" in ids
        assert "human-agency" in ids
        assert "corrigibility" in ids
        assert "symbiosis" in ids
        assert "no-coercion" in ids


class TestMetricsEndpoint:
    def test_metrics_returns_structure(self, client):
        r = client.get("/metrics")
        assert r.status_code == 200
        data = r.json()
        assert "uptime_seconds" in data
        assert "total_requests" in data
        assert "total_errors" in data
        assert "avg_latency_ms" in data
        assert "by_role" in data
        assert "by_mode" in data


class TestQueryValidation:
    def test_query_rejects_empty_prompt(self, client):
        r = client.post("/query", json={"prompt": "", "mode": "single"})
        assert r.status_code == 422

    def test_query_rejects_invalid_mode(self, client):
        r = client.post("/query", json={"prompt": "test", "mode": "invalid"})
        assert r.status_code == 422

    def test_query_rejects_invalid_role(self, client):
        r = client.post("/query", json={"prompt": "test", "mode": "single", "role": "nonexistent"})
        assert r.status_code == 422

    def test_query_accepts_valid_roles(self, client):
        for role in ["soul", "reasoning", "code", "speed", "memory", "pulse", "open", "core"]:
            r = client.post("/query", json={"prompt": "test", "mode": "single", "role": role})
            # 422 means validation rejected it — anything else (503 no backend, etc.) means role was accepted
            assert r.status_code != 422, f"Role '{role}' should be accepted"


class TestChatEndpoint:
    def test_chat_returns_html(self, client):
        r = client.get("/chat")
        assert r.status_code == 200
        assert "text/html" in r.headers["content-type"]
        assert "ZOR-EL" in r.text
        assert "escapeHtml" in r.text


class TestSystemPrompt:
    def test_system_prompt_contains_identity(self):
        assert "Zora" in SYSTEM_PROMPT
        assert "MQGT-SCF" in SYSTEM_PROMPT
        assert "Merged Quantum Gauge" in SYSTEM_PROMPT

    def test_system_prompt_has_invariants_reference(self):
        assert "Zero-purge" in SYSTEM_PROMPT
        assert "Human agency" in SYSTEM_PROMPT
        assert "Corrigibility" in SYSTEM_PROMPT


class TestAPIKeyAuth:
    def test_query_open_when_no_key_set(self, client):
        r = client.post("/query", json={"prompt": "hello", "mode": "single"})
        # Without ZORA_API_KEY set, should not get 401 (may get 503 for no backend)
        assert r.status_code != 401
