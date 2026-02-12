"""Tests for config.py — feature flags and defaults."""


def test_config_defaults(monkeypatch):
    """Config loads with safe defaults when no env vars set."""
    # Remove test-level WHISPER_ON override so we verify the true default
    monkeypatch.delenv("WHISPER_ON", raising=False)
    from src.core.config import Config
    c = Config()
    assert c.DEMO_MODE is False
    assert c.LLM_LIVE is True
    assert c.WHISPER_ON is True
    assert c.LLM_TIMEOUT == 6
    assert c.WHISPER_TIMEOUT == 12
    assert c.FLASK_ENV == "development"
    assert c.LOG_LEVEL == "INFO"


def test_config_demo_mode(monkeypatch):
    """DEMO_MODE flag reads from env."""
    monkeypatch.setenv("DEMO_MODE", "true")
    from src.core.config import Config
    c = Config()
    assert c.DEMO_MODE is True


def test_config_twilio_sandbox_default():
    """Twilio sandbox default is WhatsApp number."""
    from src.core.config import Config
    c = Config()
    assert c.TWILIO_SANDBOX_FROM == "whatsapp:+14155238886"
