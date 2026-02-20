"""Tests for ack_image and vision_fail templates."""

from src.core.prompts.templates import get_template


def test_ack_image_template_exists():
    result = get_template("ack_image", "es")
    assert "imagen" in result.lower()


def test_ack_image_template_french():
    result = get_template("ack_image", "fr")
    assert len(result) > 0


def test_vision_fail_template_exists():
    result = get_template("vision_fail", "es")
    assert len(result) > 0


def test_vision_fail_template_french():
    result = get_template("vision_fail", "fr")
    assert len(result) > 0
