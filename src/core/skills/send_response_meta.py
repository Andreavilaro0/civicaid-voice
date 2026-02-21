"""Send final response to user via Meta WhatsApp Cloud API."""

import requests
from src.core.models import FinalResponse
from src.core.config import config
from src.utils.logger import log_rest, log_error
from src.utils.timing import timed

META_API_URL = "https://graph.facebook.com/v21.0"


@timed("send_response_meta")
def send_final_message_meta(response: FinalResponse) -> bool:
    """Send text + optional media to user via Meta Cloud API. Returns True on success."""
    headers = {
        "Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }
    url = f"{META_API_URL}/{config.META_PHONE_NUMBER_ID}/messages"

    try:
        # Send text message
        payload = {
            "messaging_product": "whatsapp",
            "to": response.to_number,
            "type": "text",
            "text": {"body": response.body},
        }

        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
        log_rest(response.to_number, response.source, response.total_ms)

        # If there's a media URL, send it as a separate message
        if response.media_url:
            _send_media(url, headers, response)

        return True

    except Exception as e:
        log_error("send_response_meta", str(e))
        # Retry once (text only)
        try:
            payload = {
                "messaging_product": "whatsapp",
                "to": response.to_number,
                "type": "text",
                "text": {"body": response.body},
            }
            resp = requests.post(url, json=payload, headers=headers, timeout=10)
            resp.raise_for_status()
            log_rest(response.to_number, response.source, response.total_ms)
            return True
        except Exception as e2:
            log_error("send_response_meta_retry", str(e2))
            return False


def _send_media(url: str, headers: dict, response: FinalResponse) -> None:
    """Send audio/media as a separate WhatsApp message."""
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": response.to_number,
            "type": "audio",
            "audio": {"link": response.media_url},
        }
        resp = requests.post(url, json=payload, headers=headers, timeout=10)
        resp.raise_for_status()
    except Exception as e:
        log_error("send_media_meta", str(e))


def fetch_media_meta(media_id: str) -> bytes | None:
    """Download media from Meta Cloud API using media ID.

    Meta requires two API calls:
    1. GET /{media_id} → returns download URL
    2. GET {download_url} → returns binary content
    """
    headers = {
        "Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}",
    }

    try:
        # Step 1: Get download URL
        url_resp = requests.get(
            f"{META_API_URL}/{media_id}",
            headers=headers,
            timeout=5,
        )
        url_resp.raise_for_status()
        download_url = url_resp.json().get("url")
        if not download_url:
            log_error("fetch_media_meta", "No download URL in response")
            return None

        # Step 2: Download binary
        media_resp = requests.get(download_url, headers=headers, timeout=10)
        media_resp.raise_for_status()
        return media_resp.content

    except Exception as e:
        log_error("fetch_media_meta", str(e))
        return None
