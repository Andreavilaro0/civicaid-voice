"""Root conftest — set test-safe env before any src imports."""

import os

# Disable Whisper model loading during tests (slow, may not be installed)
os.environ.setdefault("WHISPER_ON", "false")

# Test-safe defaults — override .env to prevent auth/config interference
os.environ["TWILIO_AUTH_TOKEN"] = ""  # Disable signature validation in tests
os.environ["DEMO_MODE"] = "false"     # Tests expect DEMO_MODE off by default
os.environ["LLM_LIVE"] = "true"       # Tests expect LLM_LIVE on by default
