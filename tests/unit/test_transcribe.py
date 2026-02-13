"""Tests for transcribe.py — get_whisper_model and flag consistency."""


def test_whisper_model_none_when_disabled(monkeypatch):
    """get_whisper_model returns None when WHISPER_ON=false, even if key is set."""
    monkeypatch.setenv("WHISPER_ON", "false")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    from src.core.config import Config
    monkeypatch.setattr("src.core.skills.transcribe.config", Config())
    from src.core.skills.transcribe import get_whisper_model
    assert get_whisper_model() is None


def test_whisper_model_truthy_when_enabled(monkeypatch):
    """get_whisper_model returns truthy when WHISPER_ON=true and key is set."""
    monkeypatch.setenv("WHISPER_ON", "true")
    monkeypatch.setenv("GEMINI_API_KEY", "test-key")
    from src.core.config import Config
    monkeypatch.setattr("src.core.skills.transcribe.config", Config())
    from src.core.skills.transcribe import get_whisper_model
    assert get_whisper_model() is not None


def test_whisper_model_none_when_no_key(monkeypatch):
    """get_whisper_model returns None when no Gemini key, even if WHISPER_ON=true."""
    monkeypatch.setenv("WHISPER_ON", "true")
    monkeypatch.setenv("GEMINI_API_KEY", "")
    from src.core.config import Config
    monkeypatch.setattr("src.core.skills.transcribe.config", Config())
    from src.core.skills.transcribe import get_whisper_model
    assert get_whisper_model() is None
