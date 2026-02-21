"""Text-to-Speech — triple engine: ElevenLabs (premium) / Gemini (warm) / gTTS (fallback)."""

import hashlib
import os
import re
import wave

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "cache")

# ---------------------------------------------------------------------------
# ElevenLabs — premium human-quality voices for Clara
# Voice IDs: pre-selected warm female voices per language
# Model: eleven_multilingual_v2 (29 languages, natural prosody)
# ---------------------------------------------------------------------------
_ELEVENLABS_VOICE_ID = {
    "es": "XB0fDUnXU5powFXDhCwa",  # Charlotte — warm, natural, empathetic
    "fr": "XB0fDUnXU5powFXDhCwa",  # Charlotte — works beautifully in French
    "en": "21m00Tcm4TlvDq8ikWAM",  # Rachel — calm, reassuring
    "pt": "XB0fDUnXU5powFXDhCwa",  # Charlotte — warm multilingual
    "ar": "21m00Tcm4TlvDq8ikWAM",  # Rachel — calm, clear for Arabic
}

_ELEVENLABS_MODEL = "eleven_turbo_v2_5"

# ---------------------------------------------------------------------------
# Gemini TTS — Clara voice persona (fallback if ElevenLabs unavailable)
# Format: Audio Profile → Scene → Director's Notes → Pacing
# ---------------------------------------------------------------------------
_GEMINI_VOICE_STYLE = {
    "es": (
        "Eres Clara. Hablas como una amiga de 30 anos que trabaja en el ayuntamiento. "
        "Estas en una cafeteria tranquila explicando un tramite a alguien que confias. "
        "Tu voz es natural, cercana, nunca profesional ni de call center. "
        "Habla a ritmo de conversacion real: ni lento ni rapido, como si hablaras con tu hermana. "
        "Sonrie con la voz cuando des animo. Usa micro-pausas naturales entre ideas. "
        "Cuando dices algo empatico, baja un poco el tono y suaviza. "
        "Cuando das pasos concretos, se clara y firme pero sin perder la calidez. "
        "No leas, cuenta. No informes, explica. No recites, conversa."
    ),
    "fr": (
        "Tu es Clara. Tu parles comme une amie de 30 ans qui travaille a la mairie. "
        "Tu es dans un cafe calme, expliquant une demarche a quelqu'un en qui tu as confiance. "
        "Ta voix est naturelle, proche, jamais professionnelle ni de centre d'appel. "
        "Parle au rythme d'une vraie conversation: ni lent ni rapide. "
        "Quand tu dis quelque chose d'empathique, adoucis un peu le ton. "
        "Quand tu donnes des etapes concretes, sois claire mais chaleureuse. "
        "Ne lis pas, raconte. N'informe pas, explique. Ne recite pas, converse."
    ),
    "en": (
        "You are Clara. You speak like a 30-year-old friend who works at city hall. "
        "You are in a quiet coffee shop explaining a process to someone you care about. "
        "Your voice is natural, close, never professional or call-center-like. "
        "Speak at a real conversation pace: not slow, not fast, like talking to your sister. "
        "Smile with your voice when encouraging. Use natural micro-pauses between ideas. "
        "When saying something empathetic, soften your tone slightly. "
        "When giving concrete steps, be clear and steady but still warm. "
        "Don't read, tell. Don't inform, explain. Don't recite, converse."
    ),
    "pt": (
        "Tu es a Clara. Falas como uma amiga de 30 anos que trabalha na camara municipal. "
        "Estas num cafe tranquilo a explicar um processo a alguem de confianca. "
        "A tua voz e natural, proxima, nunca profissional nem de call center. "
        "Fala ao ritmo de uma conversa real: nem devagar nem depressa. "
        "Quando dizes algo empatico, suaviza um pouco o tom. "
        "Quando das passos concretos, se clara mas sem perder o carinho. "
        "Nao leias, conta. Nao informes, explica. Nao recites, conversa."
    ),
    "ar": (
        "You are Clara. You speak like a warm 30-year-old friend helping someone navigate paperwork. "
        "You are in a quiet, safe place having a real conversation in Arabic. "
        "Your voice is natural, close, never formal or robotic. "
        "Speak at a real conversation pace: not slow, not fast. "
        "When saying something empathetic, soften your tone gently. "
        "When giving concrete steps, be clear but still caring. "
        "Don't read, tell. Don't inform, explain. Don't recite, converse."
    ),
}

_GEMINI_VOICE_NAME = {
    "es": "Aoede",      # "Breezy" — relaxed, natural, like a real friend
    "fr": "Despina",    # "Smooth" — gentle, ideal for empathetic French
    "en": "Aoede",      # "Breezy" — natural conversational warmth
    "pt": "Aoede",      # "Breezy" — natural, close
    "ar": "Achernar",   # "Soft" — soft and warm for Arabic
}

# Max words to send to TTS — keeps audio under ~15 seconds
_TTS_MAX_WORDS = 45


def _strip_formatting(text: str) -> str:
    """Remove WhatsApp formatting that sounds bad when spoken aloud."""
    # Remove *bold* markers
    result = re.sub(r'\*([^*]+)\*', r'\1', text)
    # Remove URLs
    result = re.sub(r'https?://\S+', '', result)
    # Remove phone numbers like 060, 900 xxx xxx
    result = re.sub(r'\b\d{3}[\s-]?\d{3}[\s-]?\d{3}\b', '', result)
    # Remove standalone short numbers (like "060") at end of sentences
    result = re.sub(r'\b060\b', 'cero sesenta', result)
    # Remove [C1], [C2] citation markers
    result = re.sub(r'\[C\d+\]', '', result)
    # Clean up numbered list formatting: "1. " → "Primero, "
    result = re.sub(r'^\s*\d+\.\s*', '', result, flags=re.MULTILINE)
    # Remove multiple spaces and blank lines
    result = re.sub(r'\n{2,}', '. ', result)
    result = re.sub(r'\s{2,}', ' ', result)
    return result.strip()


def _truncate_for_tts(text: str) -> str:
    """Keep only the first ~80 words for TTS.

    Clara's responses follow E-V-I pattern (Empathy-Validate-Inform).
    We keep the empathy + validation + first few steps, which is the
    most important part for audio. Full details are in the text message.
    """
    words = text.split()
    if len(words) <= _TTS_MAX_WORDS:
        return text
    # Cut at word boundary, add natural closing
    truncated = " ".join(words[:_TTS_MAX_WORDS])
    # Try to end at a sentence boundary
    last_period = truncated.rfind(".")
    last_question = truncated.rfind("?")
    cut_point = max(last_period, last_question)
    if cut_point > len(truncated) // 2:
        truncated = truncated[:cut_point + 1]
    return truncated


def _prepare_text_for_tts(text: str) -> str:
    """Pre-process text for natural TTS: strip formatting, truncate, add pauses."""
    result = _strip_formatting(text)
    result = _truncate_for_tts(result)
    # Add micro-pause before parenthetical explanations
    result = re.sub(r'\(', '... (', result)
    return result


def _build_url(filename: str) -> str | None:
    if not config.AUDIO_BASE_URL:
        return None
    return f"{config.AUDIO_BASE_URL.rstrip('/')}/{filename}"


def _cache_path(text: str, lang: str, ext: str) -> tuple[str, str]:
    """Return (filepath, filename) based on content hash."""
    text_hash = hashlib.md5(f"{text}:{lang}".encode()).hexdigest()[:12]
    filename = f"tts_{text_hash}.{ext}"
    filepath = os.path.join(_CACHE_DIR, filename)
    return filepath, filename


def _pcm_to_wav(pcm_data: bytes, sample_rate: int = 24000) -> bytes:
    """Convert raw PCM 16-bit mono to WAV bytes."""
    import io
    buf = io.BytesIO()
    with wave.open(buf, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)  # 16-bit
        wf.setframerate(sample_rate)
        wf.writeframes(pcm_data)
    return buf.getvalue()


# ---------------------------------------------------------------------------
# Engine: ElevenLabs (premium human-quality TTS)
# ---------------------------------------------------------------------------
def _synthesize_elevenlabs(text: str, language: str) -> bytes | None:
    """Call ElevenLabs TTS. Returns MP3 bytes or None on failure."""
    if not config.ELEVENLABS_API_KEY:
        return None

    try:
        from elevenlabs import ElevenLabs

        client = ElevenLabs(api_key=config.ELEVENLABS_API_KEY)
        voice_id = _ELEVENLABS_VOICE_ID.get(language, _ELEVENLABS_VOICE_ID["es"])

        audio_gen = client.text_to_speech.convert(
            voice_id=voice_id,
            text=text,
            model_id=_ELEVENLABS_MODEL,
            output_format="mp3_22050_32",
        )
        return b"".join(audio_gen)

    except Exception as e:
        log_error("elevenlabs_tts", str(e))
        return None


# ---------------------------------------------------------------------------
# Engine: Gemini TTS (warm Clara voice)
# ---------------------------------------------------------------------------
def _synthesize_gemini(text: str, language: str) -> bytes | None:
    """Call Gemini TTS. Returns WAV bytes or None on failure.

    Expects pre-processed text (already stripped and truncated).
    """
    if not config.GEMINI_API_KEY:
        return None

    try:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        voice_name = _GEMINI_VOICE_NAME.get(language, "Sulafat")
        style = _GEMINI_VOICE_STYLE.get(language, _GEMINI_VOICE_STYLE["es"])

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=text,
            config=genai.types.GenerateContentConfig(
                response_modalities=["AUDIO"],
                speech_config=genai.types.SpeechConfig(
                    voice_config=genai.types.VoiceConfig(
                        prebuilt_voice_config=genai.types.PrebuiltVoiceConfig(
                            voice_name=voice_name
                        )
                    )
                ),
                system_instruction=style,
            ),
        )

        audio_data = response.candidates[0].content.parts[0].inline_data.data

        # If already WAV, return as-is; otherwise wrap PCM in WAV header
        if b"RIFF" in audio_data[:4]:
            return audio_data
        return _pcm_to_wav(audio_data)

    except Exception as e:
        log_error("gemini_tts", str(e))
        return None


# ---------------------------------------------------------------------------
# Engine: gTTS (basic fallback)
# ---------------------------------------------------------------------------
def _synthesize_gtts(text: str, language: str) -> str | None:
    """Original gTTS synthesis. Returns filepath or None."""
    lang_map = {"es": "es", "fr": "fr", "en": "en"}
    tts_lang = lang_map.get(language, "es")
    filepath, _ = _cache_path(text, tts_lang, "mp3")

    if os.path.exists(filepath):
        return filepath

    try:
        from gtts import gTTS
        tts = gTTS(text=text, lang=tts_lang, slow=False)
        tts.save(filepath)
        return filepath
    except Exception as e:
        log_error("tts_gtts", str(e))
        return None


# ---------------------------------------------------------------------------
# Main entry point
# ---------------------------------------------------------------------------
@timed("tts")
def text_to_audio(text: str, language: str = "es") -> str | None:
    """Convert text to audio. Returns public URL or None on failure.

    Text is automatically stripped of WhatsApp formatting and truncated
    to ~80 words before synthesis (keeps audio under ~30s).

    Engine selection via TTS_ENGINE env var:
    - "elevenlabs": ElevenLabs premium voice with Gemini/gTTS fallback
    - "gemini": Gemini TTS (warm Clara voice) with gTTS fallback
    - "gtts": Original gTTS (default, backward compatible)
    """
    if not config.AUDIO_BASE_URL:
        return None

    # Prepare text ONCE — strip formatting + truncate for all engines
    prepared = _prepare_text_for_tts(text)
    if not prepared or len(prepared.strip()) < 5:
        return None

    # --- ElevenLabs TTS path (premium) ---
    if config.TTS_ENGINE == "elevenlabs":
        filepath, filename = _cache_path(prepared, language, "mp3")

        if os.path.exists(filepath):
            return _build_url(filename)

        mp3_bytes = _synthesize_elevenlabs(prepared, language)
        if mp3_bytes:
            with open(filepath, "wb") as f:
                f.write(mp3_bytes)
            return _build_url(filename)

        log_error("tts", "ElevenLabs TTS failed, falling back to Gemini")
        # Fall through to Gemini

    # --- Gemini TTS path ---
    if config.TTS_ENGINE in ("gemini", "elevenlabs"):
        filepath, filename = _cache_path(prepared, language, "wav")

        if os.path.exists(filepath):
            return _build_url(filename)

        wav_bytes = _synthesize_gemini(prepared, language)
        if wav_bytes:
            with open(filepath, "wb") as f:
                f.write(wav_bytes)
            return _build_url(filename)

        log_error("tts", "Gemini TTS failed, falling back to gTTS")

    # --- gTTS path (default or last-resort fallback) ---
    filepath, filename = _cache_path(prepared, language, "mp3")

    if os.path.exists(filepath):
        return _build_url(filename)

    result_path = _synthesize_gtts(prepared, language)
    if result_path:
        return _build_url(filename)
    return None
