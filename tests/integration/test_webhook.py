"""Tests T6-T7: Webhook parsing."""

import pytest
import time
from unittest.mock import patch, MagicMock
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


def test_webhook_ack_english_for_english_text(client):
    """ACK should be in English when user writes in English."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hello, I need help with my registration",
            "From": "whatsapp:+44712345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "Clara" in body or "moment" in body or "question" in body


def test_webhook_ack_portuguese_for_portuguese_text(client):
    """ACK should be in Portuguese when user writes in Portuguese."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Ola, preciso de ajuda com o registo",
            "From": "whatsapp:+351912345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "Clara" in body or "momento" in body or "pergunta" in body


def test_webhook_ack_arabic_for_arabic_keywords(client):
    """ACK should be in Arabic when user writes Arabic transliterated keywords."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Salam, ahlan musaada",
            "From": "whatsapp:+212612345678",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Arabic ack should contain Arabic script
        assert "\u0643\u0644\u0627\u0631\u0627" in body or "\u0644\u062d\u0638\u0629" in body or "\u0633\u0624\u0627\u0644" in body


def test_webhook_remembers_french_for_second_message(client):
    """After French first message, ambiguous second message still gets French ACK."""
    phone = "whatsapp:+33612345678"
    with patch("src.core.pipeline.process"):
        # First message: clearly French
        client.post("/webhook", data={
            "Body": "Bonjour, j'ai besoin d'aide",
            "From": phone,
            "NumMedia": "0",
        })
        # Second message: ambiguous (just a number, no language hint)
        resp = client.post("/webhook", data={
            "Body": "NIE X1234567A",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Should still be French (remembered), not Spanish
        assert "instant" in body or "cherche" in body or "ecoute" in body


def test_webhook_remembers_english_for_second_message(client):
    """After English first message, ambiguous second message still gets English ACK."""
    phone = "whatsapp:+44799999999"
    with patch("src.core.pipeline.process"):
        # First message: clearly English
        client.post("/webhook", data={
            "Body": "Hello, I need help please",
            "From": phone,
            "NumMedia": "0",
        })
        # Second message: ambiguous
        resp = client.post("/webhook", data={
            "Body": "IMV",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Should be English (remembered)
        assert "moment" in body or "question" in body or "Clara" in body


def test_webhook_image_returns_image_ack(client):
    """Image input should return ack_image template."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_image/es: "Voy a mirar tu documento"
        assert "documento" in body or "mirar" in body


def test_webhook_image_french_ack(client):
    """French speaker sending image gets French ack_image."""
    phone = "whatsapp:+33600000001"
    with patch("src.core.pipeline.process"):
        # First: establish French
        client.post("/webhook", data={
            "Body": "Bonjour",
            "From": phone,
            "NumMedia": "0",
        })
        # Then: send image
        resp = client.post("/webhook", data={
            "Body": "",
            "From": phone,
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_image/fr: "Je regarde votre document"
        assert "document" in body or "regarde" in body


def test_webhook_rejects_invalid_signature(client):
    """Webhook returns 403 for invalid Twilio signature when auth token is set."""
    mock_config = MagicMock()
    mock_config.TWILIO_AUTH_TOKEN = "fake-auth-token"
    mock_config.OBSERVABILITY_ON = False

    with patch("src.routes.webhook.config", mock_config):
        resp = client.post("/webhook", data={
            "Body": "Hola",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        }, headers={"X-Twilio-Signature": "invalid-signature"})
        assert resp.status_code == 403


# ── Multi-language ACK flow tests ──────────────────────────────────────


def test_webhook_pt_greeting_gets_pt_ack(client):
    """Portuguese greeting gets Portuguese ack_greeting."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Ola, preciso de ajuda",
            "From": "whatsapp:+351912345679",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "Clara" in body or "prazer" in body or "momento" in body


def test_webhook_ar_greeting_gets_ar_ack(client):
    """Arabic greeting gets Arabic ack."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Salam ahlan",
            "From": "whatsapp:+212600000001",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Arabic ACK should contain Arabic script
        assert "\u0643\u0644\u0627\u0631\u0627" in body or "\u0644\u062d\u0638\u0629" in body or "\u0633\u0624\u0627\u0644" in body


def test_webhook_language_switch_fr_to_es(client):
    """User switches from French to Spanish, ACK follows."""
    phone = "whatsapp:+33switch_test_1"
    with patch("src.core.pipeline.process"):
        # First: French
        client.post("/webhook", data={
            "Body": "Bonjour, j'ai besoin d'aide",
            "From": phone,
            "NumMedia": "0",
        })
        # Second: Spanish
        resp = client.post("/webhook", data={
            "Body": "Hola necesito ayuda con el padron",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # Should be Spanish now
        assert "Clara" in body or "momento" in body


def test_webhook_three_en_messages_third_still_en(client):
    """Three messages from EN speaker: third ambiguous still gets EN."""
    phone = "whatsapp:+44three_msg_test"
    with patch("src.core.pipeline.process"):
        client.post("/webhook", data={
            "Body": "Hello, I need help please",
            "From": phone,
            "NumMedia": "0",
        })
        client.post("/webhook", data={
            "Body": "What about the health card?",
            "From": phone,
            "NumMedia": "0",
        })
        resp = client.post("/webhook", data={
            "Body": "NIE",
            "From": phone,
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        assert "moment" in body or "question" in body or "Clara" in body


def test_webhook_audio_from_fr_user_gets_fr_ack(client):
    """Audio from a user who previously spoke French gets French ack_audio."""
    phone = "whatsapp:+33audio_fr_test"
    with patch("src.core.pipeline.process"):
        # Establish French
        client.post("/webhook", data={
            "Body": "Bonjour",
            "From": phone,
            "NumMedia": "0",
        })
        # Send audio
        resp = client.post("/webhook", data={
            "Body": "",
            "From": phone,
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx",
            "MediaContentType0": "audio/ogg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # FR ack_audio: "Je vous ecoute. Un instant."
        assert "ecoute" in body or "instant" in body


def test_webhook_image_from_en_user_gets_en_ack(client):
    """Image from English speaker gets English ack_image."""
    phone = "whatsapp:+44image_en_test"
    with patch("src.core.pipeline.process"):
        # Establish English
        client.post("/webhook", data={
            "Body": "Hello, I need help",
            "From": phone,
            "NumMedia": "0",
        })
        # Send image
        resp = client.post("/webhook", data={
            "Body": "",
            "From": phone,
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/xxx/Media/yyy",
            "MediaContentType0": "image/jpeg",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # EN ack_image: "Let me look at your document. One second."
        assert "document" in body or "look" in body or "second" in body


def test_webhook_es_greeting_gets_ack_greeting(client):
    """Spanish greeting gets ack_greeting (not ack_text)."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "Hola",
            "From": "whatsapp:+34greeting_es",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_greeting has "encantada" or more personal intro
        assert "Clara" in body


def test_webhook_en_non_greeting_gets_ack_text(client):
    """English non-greeting gets ack_text (not ack_greeting)."""
    with patch("src.core.pipeline.process"):
        resp = client.post("/webhook", data={
            "Body": "What documents do I need for registration?",
            "From": "whatsapp:+44non_greet_en",
            "NumMedia": "0",
        })
        assert resp.status_code == 200
        body = resp.data.decode("utf-8")
        # ack_text: "Good question. Give me a moment..."
        assert "moment" in body or "question" in body
