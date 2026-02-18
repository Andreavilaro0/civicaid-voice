"""Tests for /forget admin endpoint."""

from unittest.mock import patch
import pytest
from src.app import create_app


@pytest.fixture
def client():
    """Flask test client."""
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_forget_requires_token(client):
    """Missing or wrong token returns 403."""
    with patch("src.routes.forget.config") as mock_cfg:
        mock_cfg.FORGET_TOKEN = "secret-123"
        resp = client.post("/forget", json={"phone": "+34600111222"})
        assert resp.status_code == 403


def test_forget_with_valid_token(client):
    """Valid token + phone returns 200."""
    with patch("src.routes.forget.config") as mock_cfg:
        mock_cfg.FORGET_TOKEN = "secret-123"
        mock_cfg.MEMORY_SECRET_SALT = "test-salt"
        mock_cfg.MEMORY_BACKEND = "dev"
        resp = client.post(
            "/forget",
            json={"phone": "+34600111222"},
            headers={"Authorization": "Bearer secret-123"},
        )
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "forgotten"


def test_forget_missing_phone(client):
    """Missing phone returns 400."""
    with patch("src.routes.forget.config") as mock_cfg:
        mock_cfg.FORGET_TOKEN = "secret-123"
        resp = client.post(
            "/forget",
            json={},
            headers={"Authorization": "Bearer secret-123"},
        )
        assert resp.status_code == 400


def test_forget_not_configured(client):
    """Empty FORGET_TOKEN returns 403."""
    with patch("src.routes.forget.config") as mock_cfg:
        mock_cfg.FORGET_TOKEN = ""
        resp = client.post(
            "/forget",
            json={"phone": "+34600111222"},
            headers={"Authorization": "Bearer something"},
        )
        assert resp.status_code == 403
        data = resp.get_json()
        assert data["error"] == "forget not configured"
