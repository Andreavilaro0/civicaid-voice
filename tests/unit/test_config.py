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


def test_vision_enabled_default_true():
    from src.core.config import Config
    c = Config()
    assert c.VISION_ENABLED is True


def test_vision_timeout_default():
    from src.core.config import Config
    c = Config()
    assert c.VISION_TIMEOUT == 10


def test_memory_config_defaults():
    """Memory flags have safe defaults."""
    from src.core.config import Config
    import os
    for key in ["MEMORY_BACKEND", "MEMORY_TTL_DAYS", "MEMORY_SECRET_SALT",
                "MEMORY_OPTIN_DEFAULT", "MEMORY_ENABLED", "FORGET_TOKEN"]:
        os.environ.pop(key, None)
    c = Config()
    assert c.MEMORY_ENABLED is False
    assert c.MEMORY_BACKEND == "dev"
    assert c.MEMORY_TTL_DAYS == 30
    assert c.MEMORY_SECRET_SALT == ""
    assert c.MEMORY_OPTIN_DEFAULT is False
    assert c.FORGET_TOKEN == ""
