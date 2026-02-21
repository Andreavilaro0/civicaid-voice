"""Tests for POST /api/chat and GET /api/health API endpoints.

Covers: health check, input validation, cache hit flow, response contract,
CORS preflight, and audio error handling.
"""
import pytest
from unittest.mock import patch, MagicMock
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


class TestApiHealth:
    """GET /api/health endpoint tests."""

    def test_returns_200_with_status_ok(self, client):
        resp = client.get("/api/health")
        assert resp.status_code == 200
        data = resp.get_json()
        assert data["status"] == "ok"

    def test_includes_feature_flags(self, client):
        resp = client.get("/api/health")
        data = resp.get_json()
        assert "features" in data
        for key in ("whisper", "llm", "guardrails", "demo_mode"):
            assert key in data["features"], f"Missing feature flag: {key}"


class TestApiChatValidation:
    """Input validation tests for POST /api/chat."""

    def test_rejects_empty_body(self, client):
        resp = client.post("/api/chat", json={})
        assert resp.status_code == 400
        data = resp.get_json()
        assert data["error"] == "text or audio_base64 required"

    def test_rejects_blank_text(self, client):
        resp = client.post("/api/chat", json={"text": "   "})
        assert resp.status_code == 400

    def test_rejects_null_text_no_audio(self, client):
        resp = client.post("/api/chat", json={"text": None, "audio_base64": None})
        assert resp.status_code == 400


class TestApiChatCacheHit:
    """Tests for the cache-hit happy path."""

    def test_cache_hit_returns_response(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(
                    respuesta="El IMV es una ayuda mensual de la Seguridad Social.",
                    audio_file=None,
                )
            )
            resp = client.post("/api/chat", json={"text": "Que es el IMV?"})
            assert resp.status_code == 200
            data = resp.get_json()
            assert data["response"] == "El IMV es una ayuda mensual de la Seguridad Social."
            assert data["source"] == "cache"

    def test_cache_hit_includes_audio_url_when_available(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"), \
             patch("src.routes.api_chat.config") as mock_config:
            mock_config.GUARDRAILS_ON = False
            mock_config.AUDIO_BASE_URL = "https://example.com/static/cache"
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(
                    respuesta="Respuesta con audio.",
                    audio_file="imv_es.mp3",
                )
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert data["audio_url"] == "https://example.com/static/cache/imv_es.mp3"


class TestApiChatContract:
    """Verifica que la respuesta tenga TODOS los campos del contrato API."""

    def test_response_has_all_required_keys(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            required_keys = {"response", "source", "language", "duration_ms", "audio_url", "sources"}
            assert required_keys.issubset(data.keys()), f"Faltan keys: {required_keys - data.keys()}"

    def test_sources_is_always_a_list(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert isinstance(data["sources"], list)

    def test_duration_ms_is_non_negative_integer(self, client):
        with patch("src.routes.api_chat.cache") as mock_cache, \
             patch("src.routes.api_chat.detect_language", return_value="es"):
            mock_cache.match.return_value = MagicMock(
                hit=True,
                entry=MagicMock(respuesta="Test.", audio_file=None)
            )
            resp = client.post("/api/chat", json={"text": "test"})
            data = resp.get_json()
            assert isinstance(data["duration_ms"], int)
            assert data["duration_ms"] >= 0


class TestApiChatCORS:
    """CORS configuration tests."""

    def test_cors_preflight_succeeds(self, client):
        resp = client.options("/api/chat", headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "POST",
        })
        assert resp.status_code in (200, 204)


class TestApiChatAudio:
    """Audio input handling tests."""

    def test_rejects_failed_transcription(self, client):
        with patch("src.core.skills.transcribe.transcribe") as mock_transcribe:
            mock_transcribe.return_value = MagicMock(success=False, text="")
            resp = client.post("/api/chat", json={
                "input_type": "audio",
                "audio_base64": "dGVzdA==",
            })
            assert resp.status_code == 422
