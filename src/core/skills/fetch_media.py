"""Download media (audio/image) from Twilio with auth."""

import requests
from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed


@timed("fetch_media")
def fetch_media(media_url: str) -> bytes | None:
    """Download media bytes from Twilio. Returns None on failure."""
    try:
        resp = requests.get(
            media_url,
            auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
            timeout=5,
        )
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        log_error("fetch_media", str(e))
        return None
