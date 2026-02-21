"""Integration tests for admin endpoints — Flask test_client with mocked metrics."""

import os
import pytest
from unittest.mock import patch

os.environ.setdefault("ADMIN_TOKEN", "int-test-token")

from src.app import create_app
from src.utils.rag_metrics import RAGMetrics

TOKEN = "int-test-token"


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


@pytest.fixture
def auth():
    return {"Authorization": f"Bearer {TOKEN}"}


@pytest.fixture(autouse=True)
def _patch_config():
    with patch("src.routes.admin.config") as cfg:
        cfg.ADMIN_TOKEN = TOKEN
        cfg.RAG_STALENESS_THRESHOLD_DAYS = 90
        yield cfg


@pytest.fixture
def seeded_metrics():
    m = RAGMetrics()
    m.record_retrieval(source="pgvector", latency_ms=100.0)
    m.record_retrieval(source="json_fallback", latency_ms=200.0)
    m.record_ingestion("updated")
    m.record_drift_check("stale")
    m.record_satisfaction(positive=True)
    m.record_satisfaction(positive=False)
    return m


class TestAdminIntegration:
    def test_rag_metrics_with_seeded_data(self, client, auth, seeded_metrics):
        with patch("src.utils.rag_metrics.rag_metrics", seeded_metrics):
            resp = client.get("/admin/rag-metrics", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["retrieval"]["total"] == 2
        assert data["ingestion"]["updated"] == 1

    def test_satisfaction_rate_calculated(self, client, auth, seeded_metrics):
        with patch("src.utils.rag_metrics.rag_metrics", seeded_metrics):
            resp = client.get("/admin/satisfaction", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["total"] == 2
        assert data["rate"] == 0.5

    def test_staleness_graceful_without_db(self, client, auth):
        resp = client.get("/admin/staleness", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert "stale_procedures" in data or "note" in data

    def test_ingestion_status_no_run(self, client, auth):
        resp = client.get("/admin/ingestion-status", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("last_run") is None or "note" in data

    def test_drift_status_no_run(self, client, auth):
        resp = client.get("/admin/drift-status", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert data.get("last_run") is None or "note" in data

    def test_cache_stats_graceful(self, client, auth):
        resp = client.get("/admin/cache-stats", headers=auth)
        assert resp.status_code == 200
        data = resp.get_json()
        assert isinstance(data, dict)

    def test_all_endpoints_reject_no_auth(self, client):
        endpoints = [
            "/admin/rag-metrics",
            "/admin/staleness",
            "/admin/satisfaction",
            "/admin/ingestion-status",
            "/admin/drift-status",
            "/admin/cache-stats",
        ]
        for ep in endpoints:
            resp = client.get(ep)
            assert resp.status_code == 401, f"{ep} should be 401 without auth"
