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

    return jsonify({
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
    })
