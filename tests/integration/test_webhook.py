"""Tests T6-T7: Webhook parsing."""

import pytest
import time
from unittest.mock import patch
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_t6_webhook_text(client):
    """T6: Webhook parses text POST correctly."""
    with patch("src.core.pipeline.process") as mock_process:
        resp = client.post("/webhook", data={
            "Body": "Hola",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        assert b"<Response>" in resp.data
        assert b"<Message>" in resp.data
        time.sleep(0.1)
        assert mock_process.called
        msg = mock_process.call_args[0][0]
        assert msg.body == "Hola"
        assert msg.input_type.value == "text"


def test_t7_webhook_audio(client):
    """T7: Webhook parses audio POST correctly."""
    with patch("src.core.pipeline.process") as mock_process:
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "audio/ogg",
        })
        assert resp.status_code == 200
        time.sleep(0.1)
        assert mock_process.called
        msg = mock_process.call_args[0][0]
        assert msg.input_type.value == "audio"
        assert msg.media_url is not None


def test_webhook_returns_twiml_xml(client):
    """Webhook returns valid TwiML XML."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Test",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert "application/xml" in resp.content_type
        assert b'<?xml version="1.0"' in resp.data


def test_webhook_ack_french_for_french_text(client):
    """ACK should be in French when user writes in French."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Bonjour, j'ai besoin d'aide",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        # Should contain French ACK, not Spanish
        assert "instant" in resp.data.decode("utf-8")


def test_webhook_ack_spanish_for_spanish_text(client):
    """ACK should remain Spanish for Spanish text."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hola necesito ayuda",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Greeting triggers ack_greeting (Clara intro) or ack_text (momento)
        assert "Clara" in body or "momento" in body


def test_webhook_ack_defaults_spanish_for_audio(client):
    """Audio ACK defaults to Spanish (can't detect language from audio body)."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx",
            "MediaContentType0": "audio/ogg",
        })
        assert resp.status_code == 200
        assert "momento" in resp.data.decode("utf-8")
