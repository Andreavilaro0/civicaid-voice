#!/usr/bin/env bash
# =============================================================
# run-local.sh — One-command local development server
#
# Usage:
#   ./scripts/run-local.sh                 # text-only (default)
#   INSTALL_AUDIO=1 ./scripts/run-local.sh # attempt whisper install
#
# On macOS, whisper + torch are heavy and may fail to compile.
# Text features work fine without whisper.
# In Docker/Render, whisper is always installed via Dockerfile.
# =============================================================

set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

echo "=== CivicAid Voice — Local Dev Server ==="

# 1. Check for .env
if [ ! -f ".env" ]; then
    echo ""
    echo "WARNING: No .env file found."
    if [ -f ".env.example" ]; then
        echo "  Copy the example and fill in your keys:"
        echo "    cp .env.example .env"
    fi
    echo "  Continuing with defaults (DEMO_MODE will be used)..."
    echo ""
fi

# 2. Check Python version
PYTHON_VERSION=$(python3 --version 2>&1 | grep -oE '3\.[0-9]+')
echo "Python: $(python3 --version)"

# 3. Install dependencies if needed
if [ ! -d "venv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv venv
fi

echo "Activating venv..."
source venv/bin/activate

echo "Installing core dependencies..."
pip install -q -r requirements.txt

# 4. Optional: install audio/whisper dependencies
if [ "${INSTALL_AUDIO:-0}" = "1" ]; then
    echo ""
    echo "INSTALL_AUDIO=1 detected — attempting whisper install..."
    if pip install -q "setuptools<75" wheel && \
       pip install -q --no-build-isolation -r requirements-audio.txt; then
        echo "Whisper installed successfully."
    else
        echo "WARNING: Whisper installation failed. Audio transcription disabled."
        echo "  Text features will work normally."
    fi
else
    echo "Skipping whisper (set INSTALL_AUDIO=1 to enable audio transcription)."
fi

# 5. Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "WARNING: ffmpeg not found. Audio transcription will fail."
    echo "  Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
fi

# 6. Run Flask dev server
echo ""
echo "Starting Flask development server on http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "Press Ctrl+C to stop"
echo ""

export FLASK_ENV=development
exec python3 -m flask --app src.app:create_app run --host 0.0.0.0 --port 5000 --reload
