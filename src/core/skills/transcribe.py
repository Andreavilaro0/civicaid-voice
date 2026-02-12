"""Transcribe audio using Whisper base model with enforced timeout."""

import time
import concurrent.futures
from src.core.models import TranscriptResult
from src.core.config import config
from src.utils.logger import log_whisper, log_error
from src.utils.timing import timed

_model = None
_executor = concurrent.futures.ThreadPoolExecutor(max_workers=1)


def load_whisper_model():
    """Load Whisper model at startup (called from app.py)."""
    global _model
    if not config.WHISPER_ON:
        return
    try:
        import whisper
        _model = whisper.load_model("base")
    except Exception as e:
        log_error("whisper_load", str(e))


def get_whisper_model():
    return _model


def _run_transcribe(wav_path: str) -> dict:
    """Run Whisper transcription in a thread (allows timeout)."""
    return _model.transcribe(wav_path, fp16=False)


@timed("transcribe")
def transcribe(wav_path: str) -> TranscriptResult:
    """Transcribe a WAV file with WHISPER_TIMEOUT enforcement."""
    if not config.WHISPER_ON or _model is None:
        return TranscriptResult(
            text="", language="es", duration_ms=0,
            success=False, error="Whisper disabled or not loaded"
        )

    start = time.time()
    try:
        future = _executor.submit(_run_transcribe, wav_path)
        result = future.result(timeout=config.WHISPER_TIMEOUT)
        elapsed = int((time.time() - start) * 1000)
        text = result.get("text", "").strip()
        lang = result.get("language", "es")
        log_whisper(True, elapsed, text)
        return TranscriptResult(
            text=text, language=lang, duration_ms=elapsed, success=True
        )
    except concurrent.futures.TimeoutError:
        elapsed = int((time.time() - start) * 1000)
        log_whisper(False, elapsed)
        log_error("transcribe", f"Whisper timeout after {config.WHISPER_TIMEOUT}s")
        return TranscriptResult(
            text="", language="es", duration_ms=elapsed,
            success=False, error=f"Timeout after {config.WHISPER_TIMEOUT}s"
        )
    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_whisper(False, elapsed)
        return TranscriptResult(
            text="", language="es", duration_ms=elapsed,
            success=False, error=str(e)
        )
