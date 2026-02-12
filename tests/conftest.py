"""Root conftest — set test-safe env before any src imports."""

import os

# Disable Whisper model loading during tests (slow, may not be installed)
os.environ.setdefault("WHISPER_ON", "false")
