"""GET /static/cache/<file> — serve pre-generated audio files (MP3, WAV)."""

import os
from flask import Blueprint, send_from_directory

static_bp = Blueprint("static_files", __name__)

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")

_MIME_TYPES = {
    ".mp3": "audio/mpeg",
    ".wav": "audio/wav",
    ".ogg": "audio/ogg",
}


@static_bp.route("/static/cache/<path:filename>", methods=["GET"])
def serve_cache_file(filename: str):
    ext = os.path.splitext(filename)[1].lower()
    mime = _MIME_TYPES.get(ext, "application/octet-stream")
    return send_from_directory(
        os.path.abspath(_CACHE_DIR),
        filename,
        mimetype=mime,
    )
