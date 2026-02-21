"""Send final response — dispatches to Twilio or Meta based on WHATSAPP_PROVIDER."""

from src.core.models import FinalResponse
from src.core.config import config
from src.utils.logger import log_rest, log_error
from src.utils.timing import timed


@timed("send_response")
def send_final_message(response: FinalResponse) -> bool:
    """Send text + optional media. Routes to Twilio or Meta automatically."""
    if config.WHATSAPP_PROVIDER == "meta":
        from src.core.skills.send_response_meta import send_final_message_meta
        return send_final_message_meta(response)
    return _send_via_twilio(response)


def _send_via_twilio(response: FinalResponse) -> bool:
    """Send via Twilio REST API with retry."""
    try:
        from twilio.rest import Client
        client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
        client.http_client.timeout = 10

        kwargs = {
            "body": response.body,
            "from_": config.TWILIO_SANDBOX_FROM,
            "to": response.to_number,
        }
        if response.media_url:
            kwargs["media_url"] = [response.media_url]

        client.messages.create(**kwargs)
        log_rest(response.to_number, response.source, response.total_ms)
        return True
    except Exception as e:
        log_error("send_response", str(e))
        # Retry once (without media, in case media caused the failure)
        try:
            from twilio.rest import Client
            client = Client(config.TWILIO_ACCOUNT_SID, config.TWILIO_AUTH_TOKEN)
            client.http_client.timeout = 10
            client.messages.create(
                body=response.body,
                from_=config.TWILIO_SANDBOX_FROM,
                to=response.to_number,
            )
            log_rest(response.to_number, response.source, response.total_ms)
            return True
        except Exception as e2:
            log_error("send_response_retry", str(e2))
            return False
