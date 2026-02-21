"""Meta WhatsApp Cloud API webhook — GET verification + POST message handler."""

import logging
import time
import threading
import hmac
import hashlib
from flask import Blueprint, request, jsonify, abort
from src.core.config import config
from src.core.models import IncomingMessage, InputType
from src.core import pipeline
from src.utils.logger import log_ack

logger = logging.getLogger("clara")

webhook_meta_bp = Blueprint("webhook_meta", __name__)


# ─── GET /webhook/meta — verification challenge ───────────────────────
@webhook_meta_bp.route("/webhook/meta", methods=["GET"])
def verify():
    """Meta sends a GET with hub.mode, hub.verify_token, hub.challenge."""
    mode = request.args.get("hub.mode")
    token = request.args.get("hub.verify_token")
    challenge = request.args.get("hub.challenge")

    if mode == "subscribe" and token == config.META_VERIFY_TOKEN:
        logger.info("[META-WEBHOOK] Verification OK")
        return challenge, 200
    else:
        logger.warning("[META-WEBHOOK] Verification failed (token mismatch)")
        abort(403)


# ─── POST /webhook/meta — receive messages ────────────────────────────
@webhook_meta_bp.route("/webhook/meta", methods=["POST"])
def receive():
    """Receive WhatsApp messages via Meta Cloud API webhook."""
    # Validate signature (X-Hub-Signature-256)
    _validate_signature(request)

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"status": "no_data"}), 200

    # Meta sends a complex nested payload — extract messages
    messages = _extract_messages(data)
    if not messages:
        # Could be a status update (delivered, read, etc.) — ACK silently
        return jsonify({"status": "ok"}), 200

    for msg_data in messages:
        from_number = msg_data.get("from_number", "")
        body = msg_data.get("body", "")
        media_url = msg_data.get("media_url")
        media_type = msg_data.get("media_type")
        input_type = msg_data.get("input_type", InputType.TEXT)

        msg = IncomingMessage(
            from_number=from_number,
            body=body,
            media_url=media_url,
            media_type=media_type,
            input_type=input_type,
            timestamp=time.time(),
        )

        # Attach observability request_id
        if config.OBSERVABILITY_ON:
            from src.utils.observability import get_context
            ctx = get_context()
            if ctx:
                msg.request_id = ctx.request_id

        log_ack(from_number, input_type.value)

        # Process in background thread (same as Twilio flow)
        thread = threading.Thread(target=pipeline.process, args=(msg,), daemon=True)
        thread.start()

    # Meta requires 200 within 5 seconds or it retries
    return jsonify({"status": "ok"}), 200


# ─── Helpers ───────────────────────────────────────────────────────────

def _validate_signature(req):
    """Validate X-Hub-Signature-256 from Meta. Skip if no token configured."""
    app_secret = config.META_WHATSAPP_TOKEN
    if not app_secret:
        logger.warning("[META-WEBHOOK] Signature validation skipped — no token configured")
        return

    signature = req.headers.get("X-Hub-Signature-256", "")
    if not signature.startswith("sha256="):
        logger.warning("[META-WEBHOOK] Missing or invalid signature header")
        # In production, abort(403). For development, log and continue.
        return

    expected = hmac.new(
        app_secret.encode("utf-8"),
        req.get_data(),
        hashlib.sha256,
    ).hexdigest()

    received = signature[7:]  # Strip "sha256=" prefix
    if not hmac.compare_digest(expected, received):
        logger.warning("[META-WEBHOOK] Signature mismatch")
        abort(403)


def _extract_messages(data: dict) -> list[dict]:
    """Extract messages from Meta's nested webhook payload.

    Meta payload structure:
    {
      "object": "whatsapp_business_account",
      "entry": [{
        "changes": [{
          "value": {
            "messages": [{ "from": "...", "type": "text|audio|image", ... }],
            "metadata": { "phone_number_id": "..." }
          }
        }]
      }]
    }
    """
    results = []

    if data.get("object") != "whatsapp_business_account":
        return results

    for entry in data.get("entry", []):
        for change in entry.get("changes", []):
            value = change.get("value", {})
            messages = value.get("messages", [])

            for msg in messages:
                from_number = msg.get("from", "")
                msg_type = msg.get("type", "text")

                if msg_type == "text":
                    body = msg.get("text", {}).get("body", "")
                    results.append({
                        "from_number": from_number,
                        "body": body,
                        "media_url": None,
                        "media_type": None,
                        "input_type": InputType.TEXT,
                    })

                elif msg_type == "audio":
                    audio = msg.get("audio", {})
                    media_id = audio.get("id", "")
                    mime_type = audio.get("mime_type", "audio/ogg")
                    # Meta requires a separate API call to download media
                    media_url = f"meta://{media_id}" if media_id else None
                    results.append({
                        "from_number": from_number,
                        "body": "",
                        "media_url": media_url,
                        "media_type": mime_type,
                        "input_type": InputType.AUDIO,
                    })

                elif msg_type == "image":
                    image = msg.get("image", {})
                    media_id = image.get("id", "")
                    mime_type = image.get("mime_type", "image/jpeg")
                    caption = image.get("caption", "")
                    media_url = f"meta://{media_id}" if media_id else None
                    results.append({
                        "from_number": from_number,
                        "body": caption,
                        "media_url": media_url,
                        "media_type": mime_type,
                        "input_type": InputType.IMAGE,
                    })

                elif msg_type == "interactive":
                    # Button reply from interactive menu
                    interactive = msg.get("interactive", {})
                    button_reply = interactive.get("button_reply", {})
                    button_id = button_reply.get("id", "")
                    results.append({
                        "from_number": from_number,
                        "body": button_id,
                        "media_url": None,
                        "media_type": None,
                        "input_type": InputType.TEXT,
                    })

                else:
                    # Unsupported type (sticker, location, etc.) — treat as text
                    logger.info("[META-WEBHOOK] Unsupported message type: %s", msg_type)

    return results
