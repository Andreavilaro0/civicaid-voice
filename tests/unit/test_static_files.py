"""Tests for static file serving with correct MIME types."""


def test_mime_types_map_has_mp3_wav():
    from src.routes.static_files import _MIME_TYPES
    assert _MIME_TYPES[".mp3"] == "audio/mpeg"
    assert _MIME_TYPES[".wav"] == "audio/wav"
    assert _MIME_TYPES[".ogg"] == "audio/ogg"
