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

    # --- Vision ---
    VISION_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("VISION_ENABLED", "true")))
    VISION_TIMEOUT: int = field(default_factory=lambda: int(os.getenv("VISION_TIMEOUT", "10")))

    # --- TTS ---
    TTS_ENGINE: str = field(default_factory=lambda: os.getenv("TTS_ENGINE", "gtts"))

    # --- RAG ---
    RAG_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_ENABLED", "false")))

    # --- RAG Database ---
    RAG_DB_URL: str = field(default_factory=lambda: os.getenv("RAG_DB_URL", ""))
    RAG_EMBEDDING_MODEL: str = field(default_factory=lambda: os.getenv("RAG_EMBEDDING_MODEL", "models/gemini-embedding-001"))
    RAG_EMBEDDING_DIMS: int = field(default_factory=lambda: int(os.getenv("RAG_EMBEDDING_DIMS", "768")))
    RAG_CHUNK_SIZE: int = field(default_factory=lambda: int(os.getenv("RAG_CHUNK_SIZE", "400")))
    RAG_CHUNK_OVERLAP: int = field(default_factory=lambda: int(os.getenv("RAG_CHUNK_OVERLAP", "50")))
    RAG_SIMILARITY_THRESHOLD: float = field(default_factory=lambda: float(os.getenv("RAG_SIMILARITY_THRESHOLD", "0.35")))
    RAG_TOP_K: int = field(default_factory=lambda: int(os.getenv("RAG_TOP_K", "5")))
    RAG_HYBRID_WEIGHT: float = field(default_factory=lambda: float(os.getenv("RAG_HYBRID_WEIGHT", "0.5")))

    # --- RAG Retrieval Quality (Q3) ---
    RAG_RERANK_STRATEGY: str = field(default_factory=lambda: os.getenv("RAG_RERANK_STRATEGY", "heuristic"))
    RAG_GROUNDED_PROMPTING: bool = field(default_factory=lambda: _bool(os.getenv("RAG_GROUNDED_PROMPTING", "true")))
    RAG_MAX_CHUNKS_IN_PROMPT: int = field(default_factory=lambda: int(os.getenv("RAG_MAX_CHUNKS_IN_PROMPT", "4")))

    # --- RAG Production (Q4) ---
    RAG_FALLBACK_CHAIN: bool = field(default_factory=lambda: _bool(os.getenv("RAG_FALLBACK_CHAIN", "true")))
    RAG_CACHE_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_CACHE_ENABLED", "false")))
    RAG_CACHE_TTL: int = field(default_factory=lambda: int(os.getenv("RAG_CACHE_TTL", "3600")))
    RAG_CACHE_BACKEND: str = field(default_factory=lambda: os.getenv("RAG_CACHE_BACKEND", "redis"))
    RAG_INGESTION_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_INGESTION_ENABLED", "false")))
    RAG_INGESTION_INTERVAL_HOURS: int = field(default_factory=lambda: int(os.getenv("RAG_INGESTION_INTERVAL_HOURS", "168")))
    RAG_INGESTION_MAX_SOURCES_PER_RUN: int = field(default_factory=lambda: int(os.getenv("RAG_INGESTION_MAX_SOURCES_PER_RUN", "50")))
    RAG_DRIFT_CHECK_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_DRIFT_CHECK_ENABLED", "false")))
    RAG_DRIFT_WEBHOOK_URL: str = field(default_factory=lambda: os.getenv("RAG_DRIFT_WEBHOOK_URL", ""))
    RAG_STALENESS_THRESHOLD_DAYS: int = field(default_factory=lambda: int(os.getenv("RAG_STALENESS_THRESHOLD_DAYS", "90")))
    RAG_BOE_MONITOR_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_BOE_MONITOR_ENABLED", "false")))
    RAG_METRICS_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("RAG_METRICS_ENABLED", "true")))

    # --- Memory / Personalization ---
    MEMORY_ENABLED: bool = field(default_factory=lambda: _bool(os.getenv("MEMORY_ENABLED", "false")))
    MEMORY_BACKEND: str = field(default_factory=lambda: os.getenv("MEMORY_BACKEND", "dev"))
    MEMORY_TTL_DAYS: int = field(default_factory=lambda: int(os.getenv("MEMORY_TTL_DAYS", "30")))
    MEMORY_SECRET_SALT: str = field(default_factory=lambda: os.getenv("MEMORY_SECRET_SALT", ""))
    MEMORY_OPTIN_DEFAULT: bool = field(default_factory=lambda: _bool(os.getenv("MEMORY_OPTIN_DEFAULT", "false")))
    FORGET_TOKEN: str = field(default_factory=lambda: os.getenv("FORGET_TOKEN", ""))


# Singleton — import this everywhere
config = Config()
