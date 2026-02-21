"""Integration test: webhook IMAGE ACK and pipeline dispatch."""

import time
import pytest
from unittest.mock import patch
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_webhook_image_returns_ack_image(client):
    """When user sends an image, webhook ACKs with 'analizando tu imagen'."""
    with patch("src.core.pipeline.process") as mock_process:
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        assert b"<Response>" in resp.data
        assert b"<Message>" in resp.data
        # Verify ACK contains image-specific text
        assert "imagen" in resp.data.decode("utf-8").lower()
        time.sleep(0.1)
        assert mock_process.called
        msg = mock_process.call_args[0][0]
        assert msg.input_type.value == "image"
        assert msg.media_url is not None
        assert msg.media_type == "image/jpeg"


def test_webhook_image_png(client):
    """Webhook handles PNG images correctly."""
    with patch("src.core.pipeline.process") as mock_process:
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34600000001",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/zzz",
            "MediaContentType0": "image/png",
        })
        assert resp.status_code == 200
        time.sleep(0.1)
        msg = mock_process.call_args[0][0]
        assert msg.input_type.value == "image"
        assert msg.media_type == "image/png"


def test_webhook_text_does_not_get_image_ack(client):
    """Text messages do NOT get the image ACK."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hola",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })
        body = resp.data.decode("utf-8").lower()
        assert "imagen" not in body
        # Greeting triggers ack_greeting (clara) or ack_text (momento)
        assert "clara" in body or "momento" in body
