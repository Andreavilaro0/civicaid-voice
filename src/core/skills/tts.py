"""Text-to-Speech — dual engine: Gemini TTS (warm) or gTTS (fallback)."""

import hashlib
import os
import re
import wave

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "cache")

# ---------------------------------------------------------------------------
# Clara voice persona — "directorial" system instructions (Google best practice)
# Format: Audio Profile → Scene → Director's Notes → Pacing
# ---------------------------------------------------------------------------
_GEMINI_VOICE_STYLE = {
    "es": (
        "Audio profile: Mujer espanola, 30 anos, voz media-grave, calida como miel. "
        "Escena: Clara esta sentada con un amigo en una cafeteria tranquila, "
        "explicandole un tramite con calma. No hay prisa, solo confianza. "
        "Direccion: Habla despacio, como si cada idea necesitara su propio espacio. "
        "Respira entre frases. Deja que el silencio trabaje. "
        "El tono es cercano y tranquilizador, como una amiga que te abraza con la voz. "
        "Baja la velocidad y suaviza la voz en las partes empaticas. "
        "Nunca suenes burocratica, apresurada ni robotica. "
        "El tempo es lento y liquido. Cada frase respira antes de la siguiente."
    ),
    "fr": (
        "Audio profile: Femme francaise, 30 ans, voix douce, chaleureuse, comme du velours. "
        "Scene: Clara est assise avec un ami dans un cafe calme a Paris, "
        "lui expliquant une demarche administrative avec patience et douceur. "
        "Direction: Parle lentement, en laissant respirer chaque phrase. "
        "Des pauses naturelles entre les idees, comme une conversation intime. "
        "Le ton est chaleureux et rassurant, comme une amie de confiance. "
        "Ralentis et adoucis ta voix sur les parties empathiques. "
        "Ne sois jamais bureaucratique ni pressee. "
        "Le tempo est lent, fluide, enveloppant."
    ),
    "en": (
        "Audio profile: Warm woman, early thirties, gentle mid-range voice like warm honey. "
        "Scene: Clara is sitting with a friend in a quiet coffee shop, "
        "calmly explaining a government process. There is no rush, only trust. "
        "Direction: Speak slowly, letting each thought breathe. "
        "Pause naturally between ideas, like a real conversation. "
        "The tone is warm and reassuring, like a friend who hugs you with her voice. "
        "Slow down and soften your voice on empathetic parts. "
        "Never sound bureaucratic, rushed, or robotic. "
        "The tempo is slow and fluid. Each sentence breathes before the next."
    ),
    "pt": (
        "Audio profile: Mulher calorosa, trinta anos, voz media e suave como mel. "
        "Cena: Clara esta sentada com um amigo num cafe tranquilo em Lisboa, "
        "a explicar um processo com calma e carinho. Nao ha pressa. "
        "Direcao: Fala devagar, deixando cada ideia respirar. "
        "Pausas naturais entre frases, como uma conversa intima. "
        "O tom e proximo e tranquilizador, como uma amiga de confianca. "
        "Abranda e suaviza a voz nas partes empaticas. "
        "Nunca soes burocratica nem apressada. "
        "O tempo e lento e fluido. Cada frase respira antes da seguinte."
    ),
    "ar": (
        "Audio profile: Warm woman, early thirties, gentle mid-range voice like warm honey. "
        "Scene: Clara is sitting with a friend in a quiet, peaceful place, "
        "calmly explaining an administrative process in Arabic. No rush, only care. "
        "Direction: Speak slowly and gently in Modern Standard Arabic. "
        "Let each thought breathe. Pause naturally between ideas. "
        "The tone is warm, caring, and reassuring, like a trusted friend. "
        "Slow down and soften your voice on empathetic parts. "
        "Never sound bureaucratic, rushed, or mechanical. "
        "The tempo is slow and fluid. Each sentence breathes before the next."
    ),
}

_GEMINI_VOICE_NAME = {
    "es": "Sulafat",  # Documented as "Warm" — ideal for Clara
    "fr": "Leda",     # "Youthful", soft
    "en": "Kore",     # "Firm" but warm
    "pt": "Sulafat",  # Warm (same as es, similar romance language)
    "ar": "Sulafat",  # Warm
}

# Max words to send to TTS — keeps audio under ~30 seconds
_TTS_MAX_WORDS = 80


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


@timed("tts")
def text_to_audio(text: str, language: str = "es") -> str | None:
    """Convert text to audio. Returns public URL or None on failure.

    Text is automatically stripped of WhatsApp formatting and truncated
    to ~80 words before synthesis (keeps audio under ~30s).

    Engine selection via TTS_ENGINE env var:
    - "gemini": Gemini TTS (warm Clara voice) with gTTS fallback
    - "gtts": Original gTTS (default, backward compatible)
    """
    if not config.AUDIO_BASE_URL:
        return None

    # Prepare text ONCE — strip formatting + truncate for all engines
    prepared = _prepare_text_for_tts(text)
    if not prepared or len(prepared.strip()) < 5:
        return None

    # --- Gemini TTS path ---
    if config.TTS_ENGINE == "gemini":
        filepath, filename = _cache_path(prepared, language, "wav")

        if os.path.exists(filepath):
            return _build_url(filename)

        wav_bytes = _synthesize_gemini(prepared, language)
        if wav_bytes:
            with open(filepath, "wb") as f:
                f.write(wav_bytes)
            return _build_url(filename)

        log_error("tts", "Gemini TTS failed, falling back to gTTS")

    # --- gTTS path (default or fallback) ---
    filepath, filename = _cache_path(prepared, language, "mp3")

    if os.path.exists(filepath):
        return _build_url(filename)

    result_path = _synthesize_gtts(prepared, language)
    if result_path:
        return _build_url(filename)
    return None
