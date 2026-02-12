"""Centralized configuration — reads env vars with safe defaults."""

import os
from dataclasses import dataclass, field
from dotenv import load_dotenv

load_dotenv()


def _bool(val: str) -> bool:
    return val.lower() in ("true", "1", "yes")


@dataclass(frozen=True)
class Config:
    # --- Twilio ---
    TWILIO_ACCOUNT_SID: str = field(default_factory=lambda: os.getenv("TWILIO_ACCOUNT_SID", ""))
    TWILIO_AUTH_TOKEN: str = field(default_factory=lambda: os.getenv("TWILIO_AUTH_TOKEN", ""))
    TWILIO_SANDBOX_FROM: str = field(default_factory=lambda: os.getenv("TWILIO_SANDBOX_FROM", "whatsapp:+14155238886"))

    # --- Gemini ---
    GEMINI_API_KEY: str = field(default_factory=lambda: os.getenv("GEMINI_API_KEY", ""))

    # --- Feature flags ---
    DEMO_MODE: bool = field(default_factory=lambda: _bool(os.getenv("DEMO_MODE", "false")))
    LLM_LIVE: bool = field(default_factory=lambda: _bool(os.getenv("LLM_LIVE", "true")))
    WHISPER_ON: bool = field(default_factory=lambda: _bool(os.getenv("WHISPER_ON", "true")))
    LLM_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("LLM_TIMEOUT", "6")))
    WHISPER_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("WHISPER_TIMEOUT", "12")))
    AUDIO_BASE_URL: str = field(default_factory=lambda: os.getenv("AUDIO_BASE_URL", ""))

    # --- Observability ---
    OBSERVABILITY_ON: bool = field(default_factory=lambda: _bool(os.getenv("OBSERVABILITY_ON", "true")))
    OTEL_ENDPOINT: str = field(default_factory=lambda: os.getenv("OTEL_ENDPOINT", ""))

    # --- App ---
    FLASK_ENV: str = field(default_factory=lambda: os.getenv("FLASK_ENV", "development"))
    LOG_LEVEL: str = field(default_factory=lambda: os.getenv("LOG_LEVEL", "INFO"))
    ADMIN_TOKEN: str = field(default_factory=lambda: os.getenv("ADMIN_TOKEN", ""))

    # --- Structured Outputs ---
    STRUCTURED_OUTPUT_ON: bool = field(default_factory=lambda: _bool(os.getenv("STRUCTURED_OUTPUT_ON", "false")))

    # --- Guardrails ---
    GUARDRAILS_ON: bool = field(default_factory=lambda: _bool(os.getenv("GUARDRAILS_ON", "true")))

    # --- RAG ---
    RAG_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_ENABLED", "false")))


# Singleton — import this everywhere
config = Config()
