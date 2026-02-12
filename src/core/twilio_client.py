"""Wrapper for Twilio REST API — send messages with retry and logging."""

from src.core.models import FinalResponse
from src.core.skills.send_response import send_final_message


def send(response: FinalResponse) -> bool:
    """Send final response via Twilio. Delegates to send_response skill."""
    return send_final_message(response)
