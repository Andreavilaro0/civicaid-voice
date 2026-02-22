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
            "whatsapp_provider": config.WHATSAPP_PROVIDER,
            "meta_token_set": bool(config.META_WHATSAPP_TOKEN),
            "meta_phone_id_set": bool(config.META_PHONE_NUMBER_ID),
            "tts_engine": config.TTS_ENGINE,
            "vision_enabled": config.VISION_ENABLED,
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


@health_bp.route("/debug/meta-test", methods=["GET"])
def debug_meta_test():
    """Quick diagnostic: verify Meta WhatsApp token + phone_number_id work."""
    import requests as http_req

    results = {"token_set": bool(config.META_WHATSAPP_TOKEN),
               "phone_id_set": bool(config.META_PHONE_NUMBER_ID)}

    if not config.META_WHATSAPP_TOKEN:
        results["error"] = "META_WHATSAPP_TOKEN not configured"
        return jsonify(results), 200

    # Test 1: verify token by calling /me endpoint
    try:
        r = http_req.get(
            "https://graph.facebook.com/v21.0/me",
            headers={"Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}"},
            timeout=5,
        )
        results["token_check"] = {"status": r.status_code, "body": r.json()}
    except Exception as e:
        results["token_check"] = {"error": str(e)}

    # Test 2: verify phone_number_id exists
    if config.META_PHONE_NUMBER_ID:
        try:
            r = http_req.get(
                f"https://graph.facebook.com/v21.0/{config.META_PHONE_NUMBER_ID}",
                headers={"Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}"},
                timeout=5,
            )
            results["phone_id_check"] = {"status": r.status_code, "body": r.json()}
        except Exception as e:
            results["phone_id_check"] = {"error": str(e)}

    return jsonify(results), 200
