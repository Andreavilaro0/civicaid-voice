"""Detect input type from Twilio POST: text, audio, or image."""

from src.core.models import InputType


def detect_input_type(num_media: int, media_content_type: str | None) -> InputType:
    if num_media == 0 or media_content_type is None:
        return InputType.TEXT
    if media_content_type.startswith("audio/"):
        return InputType.AUDIO
    if media_content_type.startswith("image/"):
        return InputType.IMAGE
    return InputType.TEXT
