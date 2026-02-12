FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# ffmpeg skipped — Whisper disabled on free tier to stay under 512MB RAM

WORKDIR /app

# Copy requirements first (leverage Docker cache)
COPY requirements.txt ./
# Skip requirements-audio.txt (openai-whisper + PyTorch) on Render free tier
# to stay under 512MB RAM limit. Set WHISPER_ON=false in env vars.
RUN pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 10000

# Gunicorn config:
# --timeout 120: Whisper can take up to 12s + LLM 6s + overhead
# --workers 1: Render free tier has limited RAM
# --preload: Load Whisper model at startup, not per-request
# Render sets PORT=10000 by default; fall back to 5000 for local
CMD gunicorn --bind "0.0.0.0:${PORT:-5000}" --timeout 120 --workers 1 --preload "src.app:create_app()"
