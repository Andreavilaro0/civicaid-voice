"""Send final response to user via Meta WhatsApp Cloud API."""

import requests
from src.core.models import FinalResponse
from src.core.config import config
from src.utils.logger import log_rest, log_error
from src.utils.timing import timed

META_API_URL = "https://graph.facebook.com/v21.0"


def _headers():
    return {
        "Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }


def _url():
    return f"{META_API_URL}/{config.META_PHONE_NUMBER_ID}/messages"


@timed("send_response_meta")
def send_final_message_meta(response: FinalResponse) -> bool:
    """Send text + optional media to user via Meta Cloud API. Returns True on success."""
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": response.to_number,
            "type": "text",
            "text": {"body": response.body},
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        log_rest(response.to_number, response.source, response.total_ms)

        if response.media_url:
            _send_media(response)

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
            resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
            resp.raise_for_status()
            return True
        except Exception as e2:
            log_error("send_response_meta_retry", str(e2))
            return False


def _send_media(response: FinalResponse) -> None:
    """Send audio/media as a separate WhatsApp message."""
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": response.to_number,
            "type": "audio",
            "audio": {"link": response.media_url},
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
    except Exception as e:
        log_error("send_media_meta", str(e))


# ── Welcome flow ──────────────────────────────────────────────────────

WELCOME = {
    "es": {
        "text": (
            "👋 *Hola, soy Clara.*\n\n"
            "Te ayudo con trámites sociales en España: "
            "IMV, empadronamiento, tarjeta sanitaria, NIE y más.\n\n"
            "🗣 Puedes *hablarme con audio* o *escribir* tu pregunta.\n"
            "🌍 Hablo español, francés y árabe.\n"
            "🔒 Gratis y confidencial."
        ),
        "speech": "Hola, soy Clara. Te ayudo con trámites sociales en España. Puedes hablarme o escribir tu pregunta.",
        "buttons": [
            {"id": "btn_imv", "title": "¿Qué es el IMV?"},
            {"id": "btn_empadronamiento", "title": "Empadronamiento"},
            {"id": "btn_salud", "title": "Tarjeta sanitaria"},
        ],
    },
    "fr": {
        "text": (
            "👋 *Salut, je suis Clara.*\n\n"
            "Je t'aide avec les démarches sociales en Espagne: "
            "RMV, inscription, carte sanitaire, NIE et plus.\n\n"
            "🗣 Tu peux *m'envoyer un audio* ou *écrire* ta question.\n"
            "🌍 Je parle espagnol, français et arabe.\n"
            "🔒 Gratuit et confidentiel."
        ),
        "speech": "Salut, je suis Clara. Je t'aide avec les démarches sociales en Espagne.",
        "buttons": [
            {"id": "btn_imv", "title": "Qu'est-ce que le RMV?"},
            {"id": "btn_empadronamiento", "title": "Inscription"},
            {"id": "btn_salud", "title": "Carte sanitaire"},
        ],
    },
    "ar": {
        "text": (
            "👋 *مرحبا، أنا كلارا.*\n\n"
            "أساعدك في الإجراءات الاجتماعية في إسبانيا: "
            "الحد الأدنى للدخل، التسجيل البلدي، البطاقة الصحية، NIE والمزيد.\n\n"
            "🗣 يمكنك *إرسال صوت* أو *كتابة* سؤالك.\n"
            "🌍 أتحدث الإسبانية والفرنسية والعربية.\n"
            "🔒 مجاني وسري."
        ),
        "speech": "مرحبا، أنا كلارا. أساعدك في الإجراءات الاجتماعية في إسبانيا.",
        "buttons": [
            {"id": "btn_imv", "title": "ما هو الحد الأدنى؟"},
            {"id": "btn_empadronamiento", "title": "التسجيل البلدي"},
            {"id": "btn_salud", "title": "البطاقة الصحية"},
        ],
    },
}


def send_welcome(to_number: str, language: str = "es") -> bool:
    """Send welcome text + audio + interactive menu buttons."""
    w = WELCOME.get(language, WELCOME["es"])

    # 1. Send welcome text
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": w["text"]},
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
    except Exception as e:
        log_error("send_welcome_text", str(e))
        return False

    # 2. Send welcome audio via TTS
    try:
        from src.core.skills.tts import text_to_audio
        audio_url = text_to_audio(w["speech"], language)
        if audio_url:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "audio",
                "audio": {"link": audio_url},
            }
            requests.post(_url(), json=payload, headers=_headers(), timeout=10)
    except Exception as e:
        log_error("send_welcome_audio", str(e))

    # 3. Send interactive menu
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": {
                    "es": "¿Sobre qué tema quieres preguntar?",
                    "fr": "Sur quel sujet veux-tu demander?",
                    "ar": "عن أي موضوع تريد أن تسأل؟",
                }.get(language, "¿Sobre qué tema quieres preguntar?")},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": btn}
                        for btn in w["buttons"]
                    ],
                },
            },
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
    except Exception as e:
        log_error("send_welcome_menu", str(e))

    return True


# ── Follow-up (after inactivity) ─────────────────────────────────────

FOLLOWUP = {
    "es": "¿Necesitas algo más? Estoy aquí para ayudarte.",
    "fr": "Tu as besoin d'autre chose? Je suis là pour t'aider.",
    "ar": "هل تحتاج شيئا آخر؟ أنا هنا لمساعدتك.",
}

FOLLOWUP_SPEECH = {
    "es": "¿Necesitas algo más?",
    "fr": "Tu as besoin d'autre chose?",
    "ar": "هل تحتاج شيئا آخر؟",
}

FOLLOWUP_BUTTONS = {
    "es": [
        {"id": "btn_continue", "title": "Seguir conversación"},
        {"id": "btn_restart", "title": "Reiniciar chat"},
    ],
    "fr": [
        {"id": "btn_continue", "title": "Continuer"},
        {"id": "btn_restart", "title": "Redémarrer"},
    ],
    "ar": [
        {"id": "btn_continue", "title": "متابعة المحادثة"},
        {"id": "btn_restart", "title": "إعادة تشغيل"},
    ],
}


def send_followup(to_number: str, language: str = "es") -> bool:
    """Send follow-up after inactivity: text + audio + buttons."""
    text = FOLLOWUP.get(language, FOLLOWUP["es"])
    buttons = FOLLOWUP_BUTTONS.get(language, FOLLOWUP_BUTTONS["es"])

    # 1. Send audio
    try:
        from src.core.skills.tts import text_to_audio
        speech = FOLLOWUP_SPEECH.get(language, FOLLOWUP_SPEECH["es"])
        audio_url = text_to_audio(speech, language)
        if audio_url:
            payload = {
                "messaging_product": "whatsapp",
                "to": to_number,
                "type": "audio",
                "audio": {"link": audio_url},
            }
            requests.post(_url(), json=payload, headers=_headers(), timeout=10)
    except Exception as e:
        log_error("send_followup_audio", str(e))

    # 2. Send interactive buttons
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "interactive",
            "interactive": {
                "type": "button",
                "body": {"text": text},
                "action": {
                    "buttons": [
                        {"type": "reply", "reply": btn}
                        for btn in buttons
                    ],
                },
            },
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        log_error("send_followup_menu", str(e))
        return False


# ── Media download ────────────────────────────────────────────────────

def fetch_media_meta(media_id: str) -> bytes | None:
    """Download media from Meta Cloud API using media ID (two-step)."""
    headers = {"Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}"}
    try:
        url_resp = requests.get(f"{META_API_URL}/{media_id}", headers=headers, timeout=5)
        url_resp.raise_for_status()
        download_url = url_resp.json().get("url")
        if not download_url:
            log_error("fetch_media_meta", "No download URL in response")
            return None
        media_resp = requests.get(download_url, headers=headers, timeout=10)
        media_resp.raise_for_status()
        return media_resp.content
    except Exception as e:
        log_error("fetch_media_meta", str(e))
        return None
