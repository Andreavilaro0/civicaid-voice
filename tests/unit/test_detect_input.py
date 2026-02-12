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
