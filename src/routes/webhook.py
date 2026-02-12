"""POST /webhook — receive Twilio messages, ACK immediately, process in background."""

import logging
import time
import threading
from flask import Blueprint, request, Response, abort
from twilio.request_validator import RequestValidator
from src.core.config import config
from src.core.models import IncomingMessage, InputType
from src.core.skills.detect_input import detect_input_type
from src.core.prompts.templates import get_template
from src.core import pipeline
from src.utils.logger import log_ack

logger = logging.getLogger("clara")

webhook_bp = Blueprint("webhook", __name__)


def _build_twiml(message: str) -> str:
    """Build TwiML XML response."""
    safe = message.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        '<?xml version="1.0" encoding="UTF-8"?>'
        f"<Response><Message>{safe}</Message></Response>"
    )


@webhook_bp.route("/webhook", methods=["POST"])
def webhook():
    # Validate Twilio signature (skip if auth token not configured)
    if config.TWILIO_AUTH_TOKEN:
        validator = RequestValidator(config.TWILIO_AUTH_TOKEN)
        signature = request.headers.get("X-Twilio-Signature", "")
        if not validator.validate(request.url, request.form, signature):
            logger.warning("[WEBHOOK] Invalid Twilio signature from %s", request.remote_addr)
            abort(403)
    else:
        logger.warning("[WEBHOOK] Twilio signature validation skipped — no auth token configured")

    # Parse Twilio POST
    body = request.form.get("Body", "").strip()
    from_number = request.form.get("From", "")
    try:
        num_media = int(request.form.get("NumMedia", "0"))
    except (ValueError, TypeError):
        num_media = 0
    media_url = request.form.get("MediaUrl0")
    media_type = request.form.get("MediaContentType0")

    # Detect input type
    input_type = detect_input_type(num_media, media_type)

    # Build IncomingMessage
    msg = IncomingMessage(
        from_number=from_number,
        body=body,
        media_url=media_url,
        media_type=media_type,
        input_type=input_type,
        timestamp=time.time(),
    )

    log_ack(from_number, input_type.value)

    # ACK template based on input type
    if input_type == InputType.AUDIO:
        ack_text = get_template("ack_audio", "es")
    else:
        ack_text = get_template("ack_text", "es")

    # Launch background thread for processing
    thread = threading.Thread(target=pipeline.process, args=(msg,), daemon=True)
    thread.start()

    # Return TwiML ACK immediately
    twiml = _build_twiml(ack_text)
    return Response(twiml, mimetype="application/xml")
