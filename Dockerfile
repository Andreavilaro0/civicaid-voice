FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

# Install ffmpeg (required for Whisper audio processing)
RUN apt-get update && \
    apt-get install -y --no-install-recommends ffmpeg && \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first (leverage Docker cache)
COPY requirements.txt requirements-audio.txt ./
# openai-whisper needs pkg_resources (setuptools<75) and --no-build-isolation
# to avoid pip's isolated build env pulling a newer setuptools without it
RUN pip install --no-cache-dir "setuptools<75" wheel && \
    pip install --no-cache-dir --no-build-isolation -r requirements-audio.txt && \
    pip install --no-cache-dir -r requirements.txt

# Copy application code
COPY . .

EXPOSE 5000

# Gunicorn config:
# --timeout 120: Whisper can take up to 12s + LLM 6s + overhead
# --workers 1: Render free tier has limited RAM
# --preload: Load Whisper model at startup, not per-request
CMD ["gunicorn", "--bind", "0.0.0.0:5000", "--timeout", "120", "--workers", "1", "--preload", "src.app:create_app()"]
