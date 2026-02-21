"""Tests: full pipeline with realistic questions (mocked LLM + Twilio).

Verifies the webhook → ACK → background pipeline flow works with
real user questions in multiple languages, mocking only the pipeline
background processing.
"""

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


class TestRealisticPipelineFlows:
    """End-to-end flows with real user questions."""

    def _send_whatsapp(self, client, body, phone="whatsapp:+34612345678"):
        """Send a WhatsApp message via webhook and return response."""
        with patch("src.core.pipeline.process") as mock_process:
            resp = client.post("/webhook", data={
                "Body": body,
                "From": phone,
                "NumMedia": "0",
            })
            time.sleep(0.1)
            return resp, mock_process

    # ── Spanish questions ──────────────────────────────────────

    def test_empadronamiento_question(self, client):
        resp, mock = self._send_whatsapp(client, "¿Cómo me empadrono?")
        assert resp.status_code == 200
        assert mock.called
        msg = mock.call_args[0][0]
        assert msg.body == "¿Cómo me empadrono?"

    def test_imv_question(self, client):
        resp, mock = self._send_whatsapp(client, "¿Qué es el IMV?")
        assert resp.status_code == 200
        assert mock.called

    def test_tarjeta_sanitaria_question(self, client):
        resp, mock = self._send_whatsapp(client, "Necesito la tarjeta sanitaria")
        assert resp.status_code == 200
        assert mock.called

    def test_desperate_user_not_blocked(self, client):
        """Desperate user asking for help should get through pipeline."""
        resp, mock = self._send_whatsapp(
            client,
            "Estoy desesperado, necesito ayuda con el IMV por favor",
        )
        assert resp.status_code == 200
        assert mock.called

    # ── French question with keyword ───────────────────────────

    def test_french_question_with_keyword(self, client):
        """French question with FR keyword gets French ACK."""
        resp, mock = self._send_whatsapp(
            client,
            "Bonjour, j'ai besoin d'aide",
            phone="whatsapp:+33612345678",
        )
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # French ACK: "Bonne question. Un instant, je cherche l'information."
        # But "bonjour" triggers greeting ACK:
        # "Bonjour ! Je suis Clara, ravie de vous connaitre..."
        assert "Clara" in body or "instant" in body or "Bonjour" in body

    # ── English question ───────────────────────────────────────

    def test_english_nie_question(self, client):
        resp, mock = self._send_whatsapp(
            client,
            "Hello, I need help with the NIE",
            phone="whatsapp:+44712345678",
        )
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # English greeting ACK: "Hi! I'm Clara, lovely to meet you..."
        assert "Clara" in body or "moment" in body

    # ── Chinese question (CJK detection) ───────────────────────

    def test_chinese_registration(self, client):
        resp, mock = self._send_whatsapp(
            client,
            "我需要在市政厅登记，怎么办？",
            phone="whatsapp:+8613812345678",
        )
        assert resp.status_code == 200
        assert mock.called

    # ── Greeting flow ──────────────────────────────────────────

    def test_greeting_triggers_welcome(self, client):
        """Simple greeting triggers ack_greeting template."""
        resp, _ = self._send_whatsapp(client, "Hola")
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "Clara" in body

    # ── TwiML format ───────────────────────────────────────────

    def test_response_is_twiml(self, client):
        """Webhook always returns valid TwiML XML."""
        resp, _ = self._send_whatsapp(client, "Hola")
        assert resp.status_code == 200
        assert "application/xml" in resp.content_type
        body = resp.data.decode("utf-8")
        assert "<Response>" in body
        assert "<Message>" in body

    def test_pipeline_receives_correct_message(self, client):
        """Pipeline receives IncomingMessage with correct fields."""
        resp, mock = self._send_whatsapp(
            client,
            "Necesito el padrón urgente",
            phone="whatsapp:+34699887766",
        )
        assert mock.called
        msg = mock.call_args[0][0]
        assert msg.from_number == "whatsapp:+34699887766"
        assert msg.body == "Necesito el padrón urgente"
        assert msg.input_type.value == "text"
