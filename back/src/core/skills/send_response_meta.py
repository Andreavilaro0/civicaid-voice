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


def send_audio_only(to_number: str, audio_url: str) -> bool:
    """Send just an audio message (used for async TTS after text is already sent)."""
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "audio",
            "audio": {"link": audio_url},
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
        return True
    except Exception as e:
        log_error("send_audio_only", str(e))
        return False


# ── Welcome flow ──────────────────────────────────────────────────────

WELCOME = {
    "es": {
        "text": (
            "👋 *Hola, soy Clara.*\n\n"
            "Te ayudo con trámites sociales en España: "
            "IMV, empadronamiento, tarjeta sanitaria, NIE y más.\n\n"
            "🗣 Puedes *hablarme con audio* o *escribir* tu pregunta.\n"
            "🌍 Hablo español, francés, inglés, portugués, rumano, catalán, chino y árabe.\n"
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
            "🌍 Je parle espagnol, français, anglais, portugais, roumain, catalan, chinois et arabe.\n"
            "🔒 Gratuit et confidentiel."
        ),
        "speech": "Salut, je suis Clara. Je t'aide avec les démarches sociales en Espagne.",
        "buttons": [
            {"id": "btn_imv", "title": "Qu'est-ce que le RMV?"},
            {"id": "btn_empadronamiento", "title": "Inscription"},
            {"id": "btn_salud", "title": "Carte sanitaire"},
        ],
    },
    "en": {
        "text": (
            "👋 *Hi, I'm Clara.*\n\n"
            "I help you with social services in Spain: "
            "minimum income, registration, health card, NIE and more.\n\n"
            "🗣 You can *send me a voice message* or *type* your question.\n"
            "🌍 I speak Spanish, French, English, Portuguese, Romanian, Catalan, Chinese and Arabic.\n"
            "🔒 Free and confidential."
        ),
        "speech": "Hi, I'm Clara. I help you with social services in Spain. You can talk to me or type your question.",
        "buttons": [
            {"id": "btn_imv", "title": "What is the IMV?"},
            {"id": "btn_empadronamiento", "title": "Registration"},
            {"id": "btn_salud", "title": "Health card"},
        ],
    },
    "pt": {
        "text": (
            "👋 *Olá, sou a Clara.*\n\n"
            "Ajudo-te com os trâmites sociais em Espanha: "
            "rendimento mínimo, inscrição, cartão de saúde, NIE e mais.\n\n"
            "🗣 Podes *enviar-me um áudio* ou *escrever* a tua pergunta.\n"
            "🌍 Falo espanhol, francês, inglês, português, romeno, catalão, chinês e árabe.\n"
            "🔒 Gratuito e confidencial."
        ),
        "speech": "Olá, sou a Clara. Ajudo-te com trâmites sociais em Espanha. Podes falar ou escrever a tua pergunta.",
        "buttons": [
            {"id": "btn_imv", "title": "O que é o IMV?"},
            {"id": "btn_empadronamiento", "title": "Inscrição"},
            {"id": "btn_salud", "title": "Cartão de saúde"},
        ],
    },
    "ro": {
        "text": (
            "👋 *Bună, sunt Clara.*\n\n"
            "Te ajut cu procedurile sociale din Spania: "
            "venitul minim, înregistrarea, cardul de sănătate, NIE și altele.\n\n"
            "🗣 Poți să *trimiți un mesaj vocal* sau să *scrii* întrebarea ta.\n"
            "🌍 Vorbesc spaniolă, franceză, engleză, portugheză, română, catalană, chineză și arabă.\n"
            "🔒 Gratuit și confidențial."
        ),
        "speech": "Bună, sunt Clara. Te ajut cu procedurile sociale din Spania. Poți să vorbești sau să scrii întrebarea ta.",
        "buttons": [
            {"id": "btn_imv", "title": "Ce este IMV?"},
            {"id": "btn_empadronamiento", "title": "Înregistrare"},
            {"id": "btn_salud", "title": "Card de sănătate"},
        ],
    },
    "ca": {
        "text": (
            "👋 *Hola, soc la Clara.*\n\n"
            "T'ajudo amb tràmits socials a Espanya: "
            "IMV, empadronament, targeta sanitària, NIE i més.\n\n"
            "🗣 Pots *enviar-me un àudio* o *escriure* la teva pregunta.\n"
            "🌍 Parlo castellà, francès, anglès, portuguès, romanès, català, xinès i àrab.\n"
            "🔒 Gratuït i confidencial."
        ),
        "speech": "Hola, soc la Clara. T'ajudo amb tràmits socials a Espanya. Pots parlar-me o escriure la teva pregunta.",
        "buttons": [
            {"id": "btn_imv", "title": "Què és l'IMV?"},
            {"id": "btn_empadronamiento", "title": "Empadronament"},
            {"id": "btn_salud", "title": "Targeta sanitària"},
        ],
    },
    "zh": {
        "text": (
            "👋 *你好，我是Clara。*\n\n"
            "我帮助你办理西班牙的社会事务：最低收入、登记注册、医疗卡、NIE等。\n\n"
            "🗣 你可以*发送语音*或*输入文字*提问。\n"
            "🌍 我会说西班牙语、法语、英语、葡萄牙语、罗马尼亚语、加泰罗尼亚语、中文和阿拉伯语。\n"
            "🔒 免费且保密。"
        ),
        "speech": "你好，我是Clara。我帮助你办理西班牙的社会事务。你可以语音或文字提问。",
        "buttons": [
            {"id": "btn_imv", "title": "什么是IMV？"},
            {"id": "btn_empadronamiento", "title": "居民登记"},
            {"id": "btn_salud", "title": "医疗卡"},
        ],
    },
    "ar": {
        "text": (
            "👋 *مرحبا، أنا كلارا.*\n\n"
            "أساعدك في الإجراءات الاجتماعية في إسبانيا: "
            "الحد الأدنى للدخل، التسجيل البلدي، البطاقة الصحية، NIE والمزيد.\n\n"
            "🗣 يمكنك *إرسال صوت* أو *كتابة* سؤالك.\n"
            "🌍 أتحدث الإسبانية والفرنسية والإنجليزية والبرتغالية والرومانية والكتالونية والصينية والعربية.\n"
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
    """Send welcome text immediately, then audio in background thread."""
    import threading
    w = WELCOME.get(language, WELCOME["es"])

    # 1. Send welcome text IMMEDIATELY
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

    # 2. Send welcome audio in BACKGROUND (don't block)
    def _send_welcome_audio():
        try:
            from src.core.skills.tts import text_to_audio
            audio_url = text_to_audio(w["speech"], language)
            if audio_url:
                send_audio_only(to_number, audio_url)
        except Exception as e:
            log_error("send_welcome_audio", str(e))

    t = threading.Thread(target=_send_welcome_audio, daemon=True)
    t.start()
    return True


# ── Follow-up (after inactivity) ─────────────────────────────────────

FOLLOWUP = {
    "es": "¿Necesitas algo más? Estoy aquí para ayudarte.",
    "fr": "Tu as besoin d'autre chose? Je suis là pour t'aider.",
    "en": "Do you need anything else? I'm here to help.",
    "pt": "Precisas de mais alguma coisa? Estou aqui para ajudar.",
    "ro": "Mai ai nevoie de ceva? Sunt aici să te ajut.",
    "ca": "Necessites alguna cosa més? Soc aquí per ajudar-te.",
    "zh": "还需要帮助吗？我在这里帮你。",
    "ar": "هل تحتاج شيئا آخر؟ أنا هنا لمساعدتك.",
}

FOLLOWUP_SPEECH = {
    "es": "¿Necesitas algo más?",
    "fr": "Tu as besoin d'autre chose?",
    "en": "Do you need anything else?",
    "pt": "Precisas de mais alguma coisa?",
    "ro": "Mai ai nevoie de ceva?",
    "ca": "Necessites alguna cosa més?",
    "zh": "还需要帮助吗？",
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
    "en": [
        {"id": "btn_continue", "title": "Continue"},
        {"id": "btn_restart", "title": "Restart chat"},
    ],
    "pt": [
        {"id": "btn_continue", "title": "Continuar"},
        {"id": "btn_restart", "title": "Reiniciar chat"},
    ],
    "ro": [
        {"id": "btn_continue", "title": "Continuă"},
        {"id": "btn_restart", "title": "Repornește chat"},
    ],
    "ca": [
        {"id": "btn_continue", "title": "Continuar"},
        {"id": "btn_restart", "title": "Reiniciar xat"},
    ],
    "zh": [
        {"id": "btn_continue", "title": "继续对话"},
        {"id": "btn_restart", "title": "重新开始"},
    ],
    "ar": [
        {"id": "btn_continue", "title": "متابعة المحادثة"},
        {"id": "btn_restart", "title": "إعادة تشغيل"},
    ],
}


def send_followup(to_number: str, language: str = "es") -> bool:
    """Send follow-up after inactivity: buttons first, audio in background."""
    import threading
    text = FOLLOWUP.get(language, FOLLOWUP["es"])
    buttons = FOLLOWUP_BUTTONS.get(language, FOLLOWUP_BUTTONS["es"])

    # 1. Send interactive buttons IMMEDIATELY
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
    except Exception as e:
        log_error("send_followup_menu", str(e))
        return False

    # 2. Send audio in BACKGROUND
    def _send_followup_audio():
        try:
            from src.core.skills.tts import text_to_audio
            speech = FOLLOWUP_SPEECH.get(language, FOLLOWUP_SPEECH["es"])
            audio_url = text_to_audio(speech, language)
            if audio_url:
                send_audio_only(to_number, audio_url)
        except Exception as e:
            log_error("send_followup_audio", str(e))

    t = threading.Thread(target=_send_followup_audio, daemon=True)
    t.start()
    return True


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
