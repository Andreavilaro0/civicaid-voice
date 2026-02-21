"""Tests T9-T10: End-to-end demo flows."""

import pytest
from unittest.mock import patch, MagicMock
from src.app import create_app


@pytest.fixture
def client():
    app = create_app()
    app.config["TESTING"] = True
    with app.test_client() as c:
        yield c


def test_t9_wa_text_demo_complete(client):
    """T9: Full WA text flow — POST 'Que es el IMV?' → ACK + background pipeline."""
    from src.core import cache
    has_cache = cache.get_entry_count() > 0

    with patch("twilio.rest.Client") as MockClient:
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM789")

        resp = client.post("/webhook", data={
            "Body": "Que es el IMV?",
            "From": "whatsapp:+34612345678",
            "NumMedia": "0",
        })

        # ACK returned immediately
        assert resp.status_code == 200
        assert b"<Response>" in resp.data

        if not has_cache:
            pytest.skip("demo_cache.json is empty — cache response flow not testable")

        # Poll for background thread completion (langdetect init can be slow)
        import time
        for _ in range(30):
            if instance.messages.create.called:
                break
            time.sleep(0.1)

        # Verify Twilio send was called with cache response
        assert instance.messages.create.called
        call_kwargs = instance.messages.create.call_args
        body = call_kwargs.kwargs.get("body", "")
        assert "Ingreso Mínimo Vital" in body


def test_t10_wa_audio_demo_stub(client):
    """T10: WA audio flow stub — verifies webhook accepts audio POST."""
    with patch("src.core.pipeline.process") as mock_process:
        resp = client.post("/webhook", data={
            "Body": "",
            "From": "whatsapp:+34612345678",
            "NumMedia": "1",
            "MediaUrl0": "https://api.twilio.com/2010-04-01/Accounts/AC123/Messages/MM123/Media/ME123",
            "MediaContentType0": "audio/ogg",
        })

        assert resp.status_code == 200
        assert b"audio" in resp.data.lower() or b"escuchando" in resp.data.lower() or b"<Message>" in resp.data

        import time
        time.sleep(0.1)

        assert mock_process.called
        msg = mock_process.call_args[0][0]
        assert msg.input_type.value == "audio"


def test_health_endpoint(client):
    """Health endpoint returns JSON with all components."""
    resp = client.get("/health")
    assert resp.status_code == 200
    data = resp.get_json()
    assert data["status"] == "ok"
    assert "components" in data
    assert "cache_entries" in data["components"]
    assert data["components"]["cache_entries"] >= 0


def test_static_cache_mp3(client):
    """Static file serving for cached MP3."""
    resp = client.get("/static/cache/imv_es.mp3")
    assert resp.status_code == 200
    assert resp.content_type == "audio/mpeg"
