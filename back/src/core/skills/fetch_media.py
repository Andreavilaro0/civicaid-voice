"""Download media (audio/image) from Twilio or Meta Cloud API."""

import requests
from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed


@timed("fetch_media")
def fetch_media(media_url: str) -> bytes | None:
    """Download media bytes. Supports Twilio URLs and meta:// media IDs."""
    if media_url.startswith("meta://"):
        return _fetch_from_meta(media_url[7:])  # Strip "meta://" prefix
    return _fetch_from_twilio(media_url)


def _fetch_from_twilio(media_url: str) -> bytes | None:
    """Download media bytes from Twilio."""
    try:
        resp = requests.get(
            media_url,
            auth=(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN),
            timeout=5,
        )
        resp.raise_for_status()
        return resp.content
    except Exception as e:
        log_error("fetch_media_twilio", str(e))
        return None


def _fetch_from_meta(media_id: str) -> bytes | None:
    """Download media from Meta Cloud API (two-step: get URL, then download)."""
    from src.core.skills.send_response_meta import fetch_media_meta
    return fetch_media_meta(media_id)
