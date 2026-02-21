"""Convert OGG audio to WAV for Whisper."""

import io
import tempfile
from src.utils.logger import log_error
from src.utils.timing import timed


@timed("convert_audio")
def convert_ogg_to_wav(ogg_bytes: bytes) -> str | None:
    """Convert OGG bytes to WAV file. Returns temp WAV path or None."""
    try:
        from pydub import AudioSegment
        audio = AudioSegment.from_ogg(io.BytesIO(ogg_bytes))
        wav_file = tempfile.NamedTemporaryFile(suffix=".wav", delete=False)
        audio.export(wav_file.name, format="wav")
        return wav_file.name
    except Exception as e:
        log_error("convert_audio", str(e))
        return None
