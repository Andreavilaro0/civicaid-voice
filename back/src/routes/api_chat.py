"""POST /api/chat — REST API for web frontend.

Reutiliza el pipeline existente de Clara de forma sincrona.
No duplica logica — importa directamente las skills existentes.
"""

import time
import base64
import logging
from flask import Blueprint, request, jsonify
from src.core.config import config
from src.core.models import InputType
from src.core import cache
from src.core.skills.detect_lang import detect_language
from src.core.skills.kb_lookup import kb_lookup
from src.core.skills.llm_generate import llm_generate
from src.core.skills.verify_response import verify_response
from src.core.prompts.templates import get_template

logger = logging.getLogger("clara")
api_bp = Blueprint("api", __name__, url_prefix="/api")


@api_bp.route("/chat", methods=["POST"])
def chat():
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language = data.get("language", "es")
    input_type_str = data.get("input_type", "text")
    audio_b64 = data.get("audio_base64")
    image_b64 = data.get("image_base64")

    if not text and not audio_b64 and not image_b64:
        return jsonify({"error": "text, audio_base64, or image_base64 required"}), 400

    start = time.time()

    # --- Audio transcription (si envian audio desde el frontend) ---
    if input_type_str == "audio" and audio_b64:
        try:
            from src.core.skills.transcribe import transcribe
            audio_bytes = base64.b64decode(audio_b64)
            transcript = transcribe(audio_bytes, "audio/webm")
            if transcript.success and transcript.text:
                text = transcript.text
                # Use transcription language if confidently detected (not default "es"),
                # otherwise re-detect from transcribed text for better accuracy
                if transcript.language and transcript.language != "es":
                    language = transcript.language
                else:
                    detected = detect_language(text)
                    language = detected
            else:
                return jsonify({"error": "audio_transcription_failed"}), 422
        except Exception as e:
            logger.error("API audio error: %s", e)
            return jsonify({"error": "audio_processing_error"}), 500

    # --- Image analysis (si envian imagen/documento desde el frontend) ---
    if input_type_str == "image" and image_b64:
        try:
            from src.core.skills.analyze_image import analyze_image
            image_bytes = base64.b64decode(image_b64)
            result = analyze_image(image_bytes, "image/jpeg", language)
            if result.success and result.text:
                elapsed = int((time.time() - start) * 1000)
                # Generate TTS for the analysis
                audio_url = None
                try:
                    from src.core.skills.tts import text_to_audio
                    audio_url = text_to_audio(result.text, language)
                except Exception:
                    pass
                return jsonify({
                    "response": result.text,
                    "source": "llm",
                    "language": language,
                    "duration_ms": elapsed,
                    "audio_url": audio_url,
                    "sources": [],
                })
            else:
                elapsed = int((time.time() - start) * 1000)
                fallback = get_template("vision_fail", language)
                return jsonify({
                    "response": fallback,
                    "source": "fallback",
                    "language": language,
                    "duration_ms": elapsed,
                    "audio_url": None,
                    "sources": [],
                })
        except Exception as e:
            logger.error("API image error: %s", e)
            return jsonify({"error": "image_processing_error"}), 500

    # --- Guardrails pre-check ---
    if config.GUARDRAILS_ON:
        from src.core.guardrails import pre_check
        guard = pre_check(text)
        if not guard.safe:
            elapsed = int((time.time() - start) * 1000)
            return jsonify({
                "response": guard.modified_text or "No puedo ayudar con ese tema.",
                "source": "guardrail", "language": language,
                "duration_ms": elapsed, "audio_url": None, "sources": []
            })

    # --- Detect language ---
    if input_type_str == "text":
        language = detect_language(text)

    # --- Cache match ---
    cache_result = cache.match(text, language, InputType.TEXT)
    if cache_result.hit and cache_result.entry:
        elapsed = int((time.time() - start) * 1000)
        audio_url = None
        if cache_result.entry.audio_file and config.AUDIO_BASE_URL:
            audio_url = f"{config.AUDIO_BASE_URL.rstrip('/')}/{cache_result.entry.audio_file}"
        return jsonify({
            "response": cache_result.entry.respuesta,
            "source": "cache", "language": language,
            "duration_ms": elapsed, "audio_url": audio_url, "sources": []
        })

    # --- Demo mode (solo cache, sin LLM) ---
    if config.DEMO_MODE:
        elapsed = int((time.time() - start) * 1000)
        return jsonify({
            "response": get_template("fallback_generic", language),
            "source": "fallback", "language": language,
            "duration_ms": elapsed, "audio_url": None, "sources": []
        })

    # --- KB lookup + LLM generate ---
    kb_context = kb_lookup(text, language)
    llm_resp = llm_generate(text, language, kb_context)
    verified = verify_response(llm_resp.text, kb_context)

    # --- Structured output (opcional) ---
    if config.STRUCTURED_OUTPUT_ON:
        from src.core.models_structured import parse_structured_response
        parsed, display = parse_structured_response(verified)
        if parsed:
            verified = display

    # --- Guardrails post-check ---
    if config.GUARDRAILS_ON:
        from src.core.guardrails import post_check
        verified = post_check(verified)

    # --- TTS (text-to-speech, best-effort) ---
    audio_url = None
    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(verified, language)
    except Exception:
        pass

    # --- Build sources list ---
    sources = []
    if kb_context and kb_context.fuente_url:
        sources.append({"name": kb_context.tramite, "url": kb_context.fuente_url})

    elapsed = int((time.time() - start) * 1000)
    return jsonify({
        "response": verified,
        "source": "llm" if llm_resp.success else "fallback",
        "language": language,
        "duration_ms": elapsed,
        "audio_url": audio_url,
        "sources": sources,
    })


@api_bp.route("/tts", methods=["POST"])
def tts():
    """Generate TTS audio for short texts (welcome speech, topic labels).

    Request: { "text": "Hola, soy Clara", "language": "es" }
    Response: { "audio_url": "https://..." } or { "audio_url": null }
    """
    data = request.get_json(silent=True) or {}
    text = (data.get("text") or "").strip()
    language = data.get("language", "es")

    if not text or len(text) > 300:
        return jsonify({"audio_url": None}), 200

    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(text, language)
        return jsonify({"audio_url": audio_url})
    except Exception as e:
        logger.error("TTS API error: %s", e)
        return jsonify({"audio_url": None})


@api_bp.route("/health", methods=["GET"])
def api_health():
    return jsonify({
        "status": "ok",
        "features": {
            "whisper": config.WHISPER_ON,
            "llm": config.LLM_LIVE,
            "guardrails": config.GUARDRAILS_ON,
            "demo_mode": config.DEMO_MODE,
        }
    })
