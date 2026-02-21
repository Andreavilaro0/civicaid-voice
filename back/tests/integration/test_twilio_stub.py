"""Test Twilio client wrapper with mocked SDK."""

from unittest.mock import patch, MagicMock
from src.core.models import FinalResponse


def test_send_final_message_text_only():
    """Send text-only message via Twilio."""
    response = FinalResponse(
        to_number="whatsapp:+34612345678",
        body="Hola, soy Clara",
        source="cache",
        total_ms=100,
    )

    with patch("twilio.rest.Client") as MockClient:
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM123")

        from src.core.skills.send_response import send_final_message
        result = send_final_message(response)
        assert result is True
        instance.messages.create.assert_called_once()


def test_send_final_message_with_media():
    """Send message with media URL."""
    response = FinalResponse(
        to_number="whatsapp:+34612345678",
        body="Info IMV",
        media_url="https://example.com/imv_es.mp3",
        source="cache",
        total_ms=200,
    )

    with patch("twilio.rest.Client") as MockClient:
        instance = MockClient.return_value
        instance.messages.create.return_value = MagicMock(sid="SM456")

        from src.core.skills.send_response import send_final_message
        result = send_final_message(response)
        assert result is True
        call_kwargs = instance.messages.create.call_args
        assert "media_url" in call_kwargs.kwargs
