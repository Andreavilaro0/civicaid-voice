#!/usr/bin/env python3
"""Generate voiceover narration audio for Clara videos.

Supports multiple backends:
  1. ElevenLabs (best quality, $5/month for 30K chars, 10K free)
  2. Gemini TTS (already in stack, free tier)
  3. gTTS (Google Translate TTS, free, robotic but reliable)
  4. edge-tts (Microsoft Edge TTS, free, good quality)

Usage:
    python scripts/media/generate_voiceover.py "Tu voz tiene poder" output.mp3
    python scripts/media/generate_voiceover.py "Tu voz tiene poder" output.mp3 --method elevenlabs
    python scripts/media/generate_voiceover.py "Tu voz tiene poder" output.mp3 --method gtts --lang es
    python scripts/media/generate_voiceover.py "Tu voz tiene poder" output.mp3 --method edge --voice es-ES-ElviraNeural
    python scripts/media/generate_voiceover.py --script scripts/media/narration_90s.txt output.mp3
"""

import argparse
import os
import subprocess
import sys
from pathlib import Path


def load_env():
    """Load .env file."""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = val.strip().strip("'\"")


# --- Recommended voices for Clara ---
VOICE_PRESETS = {
    # ElevenLabs voice IDs (you can clone a custom voice or use these)
    "elevenlabs": {
        "es": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel - warm female
            "model_id": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.8,
        },
        "fr": {
            "voice_id": "21m00Tcm4TlvDq8ikWAM",  # Rachel multilingual
            "model_id": "eleven_multilingual_v2",
            "stability": 0.5,
            "similarity_boost": 0.8,
        },
    },
    # Microsoft Edge TTS voices (free, high quality neural voices)
    "edge": {
        "es": "es-ES-ElviraNeural",      # Spanish female, warm
        "es-calm": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",       # French female, warm
        "ar": "ar-SA-ZariyahNeural",      # Arabic female
    },
}


def voiceover_elevenlabs(text: str, output_path: str, lang: str = "es") -> str:
    """Generate voiceover using ElevenLabs.

    Free tier: 10,000 characters/month.
    Starter plan: $5/month for 30,000 characters.
    Best quality for warm, empathetic narration.
    """
    try:
        from elevenlabs import ElevenLabs
    except ImportError:
        print("Installing elevenlabs...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "elevenlabs"])
        from elevenlabs import ElevenLabs

    api_key = os.environ.get("ELEVENLABS_API_KEY")
    if not api_key:
        raise ValueError("ELEVENLABS_API_KEY not set. Get one at https://elevenlabs.io/")

    preset = VOICE_PRESETS["elevenlabs"].get(lang, VOICE_PRESETS["elevenlabs"]["es"])

    client = ElevenLabs(api_key=api_key)

    print(f"[ElevenLabs] Generating {len(text)} characters of narration in '{lang}'...")
    audio = client.text_to_speech.convert(
        voice_id=preset["voice_id"],
        model_id=preset["model_id"],
        text=text,
        voice_settings={
            "stability": preset["stability"],
            "similarity_boost": preset["similarity_boost"],
        },
    )

    # Write audio to file
    with open(output_path, "wb") as f:
        for chunk in audio:
            f.write(chunk)

    print(f"[ElevenLabs] Audio saved to {output_path}")
    return output_path


def voiceover_gtts(text: str, output_path: str, lang: str = "es") -> str:
    """Generate voiceover using gTTS (Google Translate TTS).

    Completely free. Quality is robotic but always works.
    Already in project requirements.txt.
    """
    from gtts import gTTS

    lang_map = {"es": "es", "fr": "fr", "ar": "ar", "en": "en"}
    gtts_lang = lang_map.get(lang, "es")

    print(f"[gTTS] Generating narration in '{gtts_lang}'...")
    tts = gTTS(text=text, lang=gtts_lang, slow=False)
    tts.save(output_path)
    print(f"[gTTS] Audio saved to {output_path}")
    return output_path


def voiceover_edge(text: str, output_path: str, voice: str = None, lang: str = "es") -> str:
    """Generate voiceover using Microsoft Edge TTS (via edge-tts package).

    Completely free. Neural voices, good quality.
    Requires: pip install edge-tts
    """
    try:
        import edge_tts
    except ImportError:
        print("Installing edge-tts...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "edge-tts"])
        import edge_tts

    import asyncio

    if not voice:
        voice = VOICE_PRESETS["edge"].get(lang, VOICE_PRESETS["edge"]["es"])

    print(f"[Edge TTS] Generating narration with voice '{voice}'...")

    async def _generate():
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_path)

    asyncio.run(_generate())
    print(f"[Edge TTS] Audio saved to {output_path}")
    return output_path


def voiceover_gemini(text: str, output_path: str, lang: str = "es") -> str:
    """Generate voiceover using Gemini TTS (already in the Clara stack).

    Uses the project's existing Gemini integration.
    Free tier friendly.
    """
    from google import genai
    from google.genai import types

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    print(f"[Gemini TTS] Generating narration...")
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=f"Read the following text aloud in a warm, empathetic, calm voice. Language: {lang}.\n\n{text}",
        config=types.GenerateContentConfig(
            response_modalities=["AUDIO"],
            speech_config=types.SpeechConfig(
                voice_config=types.VoiceConfig(
                    prebuilt_voice_config=types.PrebuiltVoiceConfig(
                        voice_name="Kore",  # Warm female voice
                    )
                )
            ),
        ),
    )

    # Extract audio data
    for part in response.candidates[0].content.parts:
        if part.inline_data and part.inline_data.mime_type.startswith("audio"):
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            print(f"[Gemini TTS] Audio saved to {output_path}")
            return output_path

    raise RuntimeError("Gemini did not return audio")


def generate_voiceover(
    text: str,
    output_path: str,
    method: str = "auto",
    lang: str = "es",
    voice: str = None,
) -> str:
    """Generate voiceover with automatic method selection.

    Priority: edge-tts (free+good) > ElevenLabs (paid+best) > Gemini > gTTS
    """
    load_env()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if method == "elevenlabs":
        return voiceover_elevenlabs(text, output_path, lang)
    elif method == "gtts":
        return voiceover_gtts(text, output_path, lang)
    elif method == "edge":
        return voiceover_edge(text, output_path, voice, lang)
    elif method == "gemini":
        return voiceover_gemini(text, output_path, lang)
    elif method == "auto":
        # Try edge-tts first (free + good quality)
        try:
            return voiceover_edge(text, output_path, voice, lang)
        except Exception as e:
            print(f"[Auto] Edge TTS failed: {e}", file=sys.stderr)

        # Try ElevenLabs if key available
        if os.environ.get("ELEVENLABS_API_KEY"):
            try:
                return voiceover_elevenlabs(text, output_path, lang)
            except Exception as e:
                print(f"[Auto] ElevenLabs failed: {e}", file=sys.stderr)

        # Try Gemini if key available
        if os.environ.get("GEMINI_API_KEY"):
            try:
                return voiceover_gemini(text, output_path, lang)
            except Exception as e:
                print(f"[Auto] Gemini TTS failed: {e}", file=sys.stderr)

        # Fallback to gTTS (always available)
        print("[Auto] Falling back to gTTS...", file=sys.stderr)
        return voiceover_gtts(text, output_path, lang)

    raise ValueError(f"Unknown method: {method}")


# --- Predefined narration scripts ---
NARRATION_SCRIPTS = {
    "elevator-30s": {
        "lang": "es",
        "text": (
            "En Espana viven casi diez millones de inmigrantes. "
            "Dos de cada tres enfrentan barreras burocraticas. "
            "Clara es una asistente de WhatsApp que entiende tu voz, "
            "habla tu idioma, y te explica tus derechos. "
            "Solo necesitas tu voz. Clara hace el resto. "
            "Tu voz tiene poder."
        ),
    },
    "demo-90s": {
        "lang": "es",
        "text": (
            "Cada dia, miles de personas en Espana se enfrentan a formularios que no entienden. "
            "Porque la burocracia no fue disenada para todos. "
            "Nosotros construimos a Clara. "
            "Una asistente de WhatsApp que te explica tus derechos. En tu idioma. Con tu voz. "
            "Ahmed acaba de llegar de Senegal. Manda un audio en frances preguntando como empadronarse. "
            "Clara detecta su idioma, y le responde en frances, paso a paso. "
            "Maria tiene setenta y dos anos. Recibio una carta oficial que no entiende. "
            "Le manda la foto a Clara. Clara le explica que dice, y le sugiere una ayuda adicional que no sabia que existia. "
            "Treinta y tres millones de personas usan WhatsApp en Espana. Sin descargar nada. Sin crear cuentas. "
            "Informacion verificada del gobierno. Quinientas treinta y dos pruebas automatizadas. "
            "Desplegada y funcionando. "
            "Todo el codigo es abierto y gratuito. Cualquier ayuntamiento puede desplegar a Clara manana. "
            "Sin pagar un euro. Para siempre. "
            "Tu voz tiene poder."
        ),
    },
    "hook-5s": {
        "lang": "es",
        "text": "Diez millones de inmigrantes. Dos de cada tres no navegan el papeleo.",
    },
    "closing-5s": {
        "lang": "es",
        "text": "Clara. Porque entender no deberia ser un privilegio.",
    },
    "como-usar-30s": {
        "lang": "es",
        "text": (
            "Usar Clara es muy fácil. "
            "Primero, abre WhatsApp y escribe Hola Clara. "
            "Luego, elige tu idioma: español, francés o árabe. "
            "Después, habla o escribe tu pregunta. "
            "Clara te responde al momento, paso a paso, con enlaces oficiales. "
            "Así de simple. Tu voz tiene poder."
        ),
    },
}


def main():
    parser = argparse.ArgumentParser(description="Generate voiceover narration for Clara videos")
    parser.add_argument("text", nargs="?", help="Text to narrate")
    parser.add_argument("output", nargs="?", default="voiceover.mp3", help="Output audio path")
    parser.add_argument("--method", choices=["auto", "elevenlabs", "gtts", "edge", "gemini"],
                        default="auto", help="TTS method (default: auto)")
    parser.add_argument("--lang", default="es", help="Language code: es, fr, ar, en (default: es)")
    parser.add_argument("--voice", default=None, help="Specific voice name (for edge-tts)")
    parser.add_argument("--script", help="Read text from file instead of argument")
    parser.add_argument("--preset", choices=list(NARRATION_SCRIPTS.keys()),
                        help="Use a predefined narration script")
    parser.add_argument("--list-presets", action="store_true", help="List available narration presets")
    parser.add_argument("--list-voices", action="store_true", help="List available edge-tts voices for Spanish")

    args = parser.parse_args()

    if args.list_presets:
        print("\nAvailable narration presets:\n")
        for name, cfg in NARRATION_SCRIPTS.items():
            preview = cfg["text"][:80] + "..."
            print(f"  {name:20s} [{cfg['lang']}]  {preview}\n")
        return

    if args.list_voices:
        try:
            import edge_tts
            import asyncio

            async def _list():
                voices = await edge_tts.list_voices()
                for v in voices:
                    if v["Locale"].startswith("es-"):
                        print(f"  {v['ShortName']:30s}  {v['Gender']:8s}  {v['Locale']}")
            print("\nSpanish voices in Edge TTS:\n")
            asyncio.run(_list())
        except ImportError:
            print("Install edge-tts first: pip install edge-tts", file=sys.stderr)
        return

    # Determine text
    if args.preset:
        cfg = NARRATION_SCRIPTS[args.preset]
        text = cfg["text"]
        lang = cfg["lang"]
        output = args.output if args.output != "voiceover.mp3" else f"voiceover_{args.preset}.mp3"
    elif args.script:
        with open(args.script) as f:
            text = f.read().strip()
        lang = args.lang
        output = args.output
    elif args.text:
        text = args.text
        lang = args.lang
        output = args.output
    else:
        parser.print_help()
        sys.exit(1)

    generate_voiceover(text, output, args.method, lang, args.voice)


if __name__ == "__main__":
    main()
