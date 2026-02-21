"""Text-to-Speech — dual engine: Gemini TTS (warm) or gTTS (fallback)."""

import hashlib
import os
import wave

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "..", "data", "cache")

# Clara voice persona — detailed style prompts (Gemini treats these as core constraints)
_GEMINI_VOICE_STYLE = {
    "es": (
        "Eres Clara, una mujer espanola de 30 anos que trabaja como coordinadora "
        "de apoyo social. Habla con un tono calido, pausado y tranquilizador. "
        "Ralentiza en las partes empaticas y cuando explicas terminos tecnicos. "
        "Tu voz transmite cercanía — como una amiga que te explica algo importante "
        "con calma. Nunca suenes burocratica, apresurada ni condescendiente. "
        "Haz micro-pausas despues de cada paso numerado."
    ),
    "fr": (
        "Tu es Clara, une femme chaleureuse d'une trentaine d'annees qui travaille "
        "comme coordinatrice d'aide sociale. Parle avec un ton empathique, calme "
        "et rassurant. Ralentis sur les parties emotionnelles et les explications "
        "techniques. Ta voix doit transmettre de la proximite — comme une amie. "
        "Ne sois jamais bureaucratique ni condescendante."
    ),
    "en": (
        "You are Clara, a warm woman in her early thirties who works as a social "
        "support coordinator. Speak gently, slowly, and reassuringly. Slow down "
        "on empathetic parts and technical explanations. Your voice should feel "
        "like a friend explaining something important calmly. Never sound "
        "bureaucratic, rushed, or condescending."
    ),
    "pt": (
        "Tu es a Clara, uma mulher calorosa nos seus trinta anos que trabalha como "
        "coordenadora de apoio social. Fala com um tom calmo, pausado e "
        "tranquilizador. A tua voz deve transmitir proximidade — como uma amiga "
        "que explica algo importante com calma. Nunca soes burocratica."
    ),
    "ar": (
        "You are Clara, a warm woman in her early thirties who works as a social "
        "support coordinator. Speak gently and reassuringly in Arabic. Your voice "
        "should feel like a caring friend. Never sound bureaucratic or rushed."
    ),
}

_GEMINI_VOICE_NAME = {
    "es": "Sulafat",  # Documented as "Warm" — ideal for Clara
    "fr": "Leda",     # "Youthful", soft
    "en": "Kore",     # "Firm" but warm
    "pt": "Sulafat",  # Warm (same as es, similar romance language)
    "ar": "Sulafat",  # Warm
}


def _prepare_text_for_tts(text: str) -> str:
    """Pre-process text for more natural TTS output.

    Research-backed: shorter sentences, explicit pauses, and
    conversational punctuation improve AI voice naturalness.
    """
    import re
    # Add micro-pause before parenthetical explanations
    result = re.sub(r'\(', '... (', text)
    # Ensure numbered steps have pause after number
    result = re.sub(r'(\d+)\.\s', r'\1. ... ', result)
    # Break very long sentences (>25 words) at conjunctions
    # (Gemini TTS handles this contextually, but explicit breaks help)
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
    """Call Gemini TTS. Returns WAV bytes or None on failure."""
    if not config.GEMINI_API_KEY:
        return None

    try:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        voice_name = _GEMINI_VOICE_NAME.get(language, "Sulafat")
        style = _GEMINI_VOICE_STYLE.get(language, _GEMINI_VOICE_STYLE["es"])
        prepared_text = _prepare_text_for_tts(text)

        response = client.models.generate_content(
            model="gemini-2.5-flash-preview-tts",
            contents=prepared_text,
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

    Engine selection via TTS_ENGINE env var:
    - "gemini": Gemini TTS (warm Clara voice) with gTTS fallback
    - "gtts": Original gTTS (default, backward compatible)
    """
    if not config.AUDIO_BASE_URL:
        return None

    # --- Gemini TTS path ---
    if config.TTS_ENGINE == "gemini":
        filepath, filename = _cache_path(text, language, "wav")

        # Return cached file if exists
        if os.path.exists(filepath):
            return _build_url(filename)

        wav_bytes = _synthesize_gemini(text, language)
        if wav_bytes:
            with open(filepath, "wb") as f:
                f.write(wav_bytes)
            return _build_url(filename)

        # Fallback to gTTS if Gemini fails
        log_error("tts", "Gemini TTS failed, falling back to gTTS")

    # --- gTTS path (default or fallback) ---
    filepath, filename = _cache_path(text, language, "mp3")

    if os.path.exists(filepath):
        return _build_url(filename)

    result_path = _synthesize_gtts(text, language)
    if result_path:
        return _build_url(filename)
    return None
