"""GET /health — component status endpoint."""

import time
import shutil
from flask import Blueprint, jsonify
from src.core import cache
from src.core.config import config
from src.core.skills.transcribe import get_whisper_model

health_bp = Blueprint("health", __name__)

_start_time = time.time()


@health_bp.route("/health", methods=["GET"])
def health():
    ffmpeg_available = shutil.which("ffmpeg") is not None
    whisper_loaded = get_whisper_model() is not None

    health_data = {
        "status": "ok",
        "uptime_s": int(time.time() - _start_time),
        "components": {
            "whisper_loaded": whisper_loaded,
            "whisper_enabled": config.WHISPER_ON,
            "ffmpeg_available": ffmpeg_available,
            "gemini_key_set": bool(config.GEMINI_API_KEY),
            "twilio_configured": bool(config.TWILIO_ACCOUNT_SID and config.TWILIO_AUTH_TOKEN),
            "cache_entries": cache.get_entry_count(),
            "demo_mode": config.DEMO_MODE,
            "llm_live": config.LLM_LIVE,
        },
    }

    # Memory status
    if config.MEMORY_ENABLED:
        from src.core.memory.store import get_store
        try:
            store = get_store(config.MEMORY_BACKEND)
            health_data["components"]["memory"] = {"status": "ok", "backend": config.MEMORY_BACKEND, "healthy": store.health()}
        except Exception as e:
            health_data["components"]["memory"] = {"status": "error", "error": str(e)}
    else:
        health_data["components"]["memory"] = {"status": "disabled"}

    return jsonify(health_data)
