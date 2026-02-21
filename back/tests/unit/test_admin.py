"""Unit tests for src/routes/admin.py — admin endpoints."""

import os
import pytest
from unittest.mock import patch

# Ensure ADMIN_TOKEN is set before config singleton is created
os.environ.setdefault("ADMIN_TOKEN", "test-token-123")

from src.app import create_app

TOKEN = "test-token-123"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def auth_headers():
    return {"Authorization": f"Bearer {TOKEN}"}


@pytest.fixture(autouse=True)
def _patch_admin_token():
    """Patch config.ADMIN_TOKEN for all tests in this module."""
    with patch("src.routes.admin.config") as mock_cfg:
        mock_cfg.ADMIN_TOKEN = TOKEN
        mock_cfg.RAG_STALENESS_THRESHOLD_DAYS = 90
        yield mock_cfg


class TestRagMetricsEndpoint:
    def test_returns_json_with_valid_token(self, client, auth_headers):
        resp = client.get("/admin/rag-metrics", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "retrieval" in data
        assert "ingestion" in data

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/rag-metrics")
        assert resp.status_code == 401
        data = resp.get_json()
        assert "error" in data

    def test_returns_401_with_wrong_token(self, client):
        resp = client.get(
            "/admin/rag-metrics",
            headers={"Authorization": "Bearer wrong-token"},
        )
        assert resp.status_code == 401


class TestStalenessEndpoint:
    def test_returns_json_with_token(self, client, auth_headers):
        resp = client.get("/admin/staleness", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "stale_procedures" in data or "note" in data

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/staleness")
        assert resp.status_code == 401


class TestSatisfactionEndpoint:
    def test_returns_rate_calculation(self, client, auth_headers):
        resp = client.get("/admin/satisfaction", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "total" in data
        assert "positive" in data
        assert "rate" in data

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/satisfaction")
        assert resp.status_code == 401


class TestIngestionStatusEndpoint:
    def test_returns_json(self, client, auth_headers):
        resp = client.get("/admin/ingestion-status", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "note" in data or "last_run" in data

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/ingestion-status")
        assert resp.status_code == 401


class TestDriftStatusEndpoint:
    def test_returns_json(self, client, auth_headers):
        resp = client.get("/admin/drift-status", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "note" in data or "last_run" in data

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/drift-status")
        assert resp.status_code == 401


class TestCacheStatsEndpoint:
    def test_returns_json(self, client, auth_headers):
        resp = client.get("/admin/cache-stats", headers=auth_headers)
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, dict)

    def test_returns_401_without_token(self, client):
        resp = client.get("/admin/cache-stats")
        assert resp.status_code == 401
