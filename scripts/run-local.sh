#!/usr/bin/env bash
# =============================================================
# run-local.sh — One-command local development server
# Usage: ./scripts/run-local.sh
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

echo "Installing dependencies..."
pip install -q -r requirements.txt

# 4. Check ffmpeg
if command -v ffmpeg &> /dev/null; then
    echo "ffmpeg: $(ffmpeg -version 2>&1 | head -1)"
else
    echo "WARNING: ffmpeg not found. Audio transcription will fail."
    echo "  Install with: brew install ffmpeg (macOS) or apt install ffmpeg (Linux)"
fi

# 5. Run Flask dev server
echo ""
echo "Starting Flask development server on http://localhost:5000"
echo "Health check: http://localhost:5000/health"
echo "Press Ctrl+C to stop"
echo ""

export FLASK_ENV=development
exec python3 -m flask --app src.app:create_app run --host 0.0.0.0 --port 5000 --reload
