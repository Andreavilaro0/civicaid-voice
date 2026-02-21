"""Tests for detect_input skill."""

from src.core.skills.detect_input import detect_input_type
from src.core.models import InputType


def test_text_input():
    assert detect_input_type(0, None) == InputType.TEXT


def test_audio_input():
    assert detect_input_type(1, "audio/ogg") == InputType.AUDIO


def test_image_input():
    assert detect_input_type(1, "image/jpeg") == InputType.IMAGE


def test_unknown_media_type():
    assert detect_input_type(1, "application/pdf") == InputType.TEXT


def test_video_input_treated_as_text():
    """Video media (not supported) falls back to text."""
    assert detect_input_type(1, "video/mp4") == InputType.TEXT


def test_multiple_media_audio():
    """Multiple media items — if first is audio, detect as audio."""
    assert detect_input_type(2, "audio/ogg") == InputType.AUDIO


def test_empty_mime_type():
    """Empty string mime_type — startswith checks return False, falls to TEXT."""
    assert detect_input_type(1, "") == InputType.TEXT


def test_zero_media_ignores_mime():
    """num_media=0 with non-None mime still returns TEXT."""
    assert detect_input_type(0, "audio/ogg") == InputType.TEXT


def test_audio_mpeg_detected():
    """audio/mpeg (MP3) detected as audio."""
    assert detect_input_type(1, "audio/mpeg") == InputType.AUDIO


def test_image_png_detected():
    """image/png detected as image."""
    assert detect_input_type(1, "image/png") == InputType.IMAGE


def test_image_webp_detected():
    """image/webp detected as image."""
    assert detect_input_type(1, "image/webp") == InputType.IMAGE
