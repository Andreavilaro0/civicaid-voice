"""GET /static/cache/<file> — serve pre-generated MP3 audio files."""

import os
from flask import Blueprint, send_from_directory

static_bp = Blueprint("static_files", __name__)

_CACHE_DIR = os.path.join(os.path.dirname(__file__), "..", "..", "data", "cache")


@static_bp.route("/static/cache/<path:filename>", methods=["GET"])
def serve_cache_file(filename: str):
    return send_from_directory(
        os.path.abspath(_CACHE_DIR),
        filename,
        mimetype="audio/mpeg",
    )
