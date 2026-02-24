"""Send final response to user via Meta WhatsApp Cloud API."""

import requests
from src.core.models import FinalResponse
from src.core.config import config
from src.utils.logger import log_rest, log_error
from src.utils.timing import timed

META_API_URL = "https://graph.facebook.com/v22.0"


def _headers():
    return {
        "Authorization": f"Bearer {config.META_WHATSAPP_TOKEN}",
        "Content-Type": "application/json",
    }


def _url():
    return f"{META_API_URL}/{config.META_PHONE_NUMBER_ID}/messages"


def _normalize_mx_number(phone: str) -> str:
    """Fix Mexican numbers: Meta webhooks send 521XXXXXXXXXX but API needs 52XXXXXXXXXX."""
    if phone.startswith("521") and len(phone) == 13:
        return "52" + phone[3:]
    return phone


@timed("send_response_meta")
def send_final_message_meta(response: FinalResponse) -> bool:
    """Send text + optional media to user via Meta Cloud API. Returns True on success."""
    try:
        to_number = _normalize_mx_number(response.to_number)
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
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
                "to": to_number,
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
        to_number = _normalize_mx_number(response.to_number)
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
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
        to_number = _normalize_mx_number(to_number)
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

LEGAL_PAGE_BASE = "https://andreavilaro0.github.io/civicaid-voice/info-legal"

WELCOME = {
    "es": {
        "text": (
            "👋 *Hola, soy Clara.*\n\n"
            "🤖 Soy una inteligencia artificial, no una persona. "
            "Mi información es orientativa y no sustituye asesoramiento profesional.\n\n"
            "Te ayudo con trámites sociales en España: "
            "IMV, empadronamiento, tarjeta sanitaria, NIE y más.\n\n"
            "🗣 Puedes *hablarme con audio* o *escribir* tu pregunta.\n"
            "🌍 Hablo español, francés, inglés, portugués, rumano, catalán, chino y árabe.\n"
            "🔒 Gratis y confidencial.\n\n"
            f"📋 Info legal: {LEGAL_PAGE_BASE}?lang=es"
        ),
        "speech": "Nadie debería quedarse solo ante un trámite. Soy Clara, una inteligencia artificial que te escucha. Cuéntame, en tu idioma.",
        "buttons": [
            {"id": "btn_imv", "title": "¿Qué es el IMV?"},
            {"id": "btn_empadronamiento", "title": "Empadronamiento"},
            {"id": "btn_salud", "title": "Tarjeta sanitaria"},
        ],
    },
    "fr": {
        "text": (
            "👋 *Salut, je suis Clara.*\n\n"
            "🤖 Je suis une intelligence artificielle, pas une personne. "
            "Mes informations sont indicatives et ne remplacent pas un conseil professionnel.\n\n"
            "Je t'aide avec les démarches sociales en Espagne: "
            "RMV, inscription, carte sanitaire, NIE et plus.\n\n"
            "🗣 Tu peux *m'envoyer un audio* ou *écrire* ta question.\n"
            "🌍 Je parle espagnol, français, anglais, portugais, roumain, catalan, chinois et arabe.\n"
            "🔒 Gratuit et confidentiel.\n\n"
            f"📋 Infos légales : {LEGAL_PAGE_BASE}?lang=fr"
        ),
        "speech": "Personne ne devrait rester seul face à une démarche. Je suis Clara, une intelligence artificielle qui t'écoute. Raconte-moi, dans ta langue.",
        "buttons": [
            {"id": "btn_imv", "title": "Qu'est-ce que le RMV?"},
            {"id": "btn_empadronamiento", "title": "Inscription"},
            {"id": "btn_salud", "title": "Carte sanitaire"},
        ],
    },
    "en": {
        "text": (
            "👋 *Hi, I'm Clara.*\n\n"
            "🤖 I am an artificial intelligence, not a person. "
            "My information is for guidance only and does not replace professional advice.\n\n"
            "I help you with social services in Spain: "
            "minimum income, registration, health card, NIE and more.\n\n"
            "🗣 You can *send me a voice message* or *type* your question.\n"
            "🌍 I speak Spanish, French, English, Portuguese, Romanian, Catalan, Chinese and Arabic.\n"
            "🔒 Free and confidential.\n\n"
            f"📋 Legal info: {LEGAL_PAGE_BASE}?lang=en"
        ),
        "speech": "Nobody should face a procedure alone. I'm Clara, an artificial intelligence that listens to you. Tell me, in your language.",
        "buttons": [
            {"id": "btn_imv", "title": "What is the IMV?"},
            {"id": "btn_empadronamiento", "title": "Registration"},
            {"id": "btn_salud", "title": "Health card"},
        ],
    },
    "pt": {
        "text": (
            "👋 *Olá, sou a Clara.*\n\n"
            "🤖 Sou uma inteligência artificial, não uma pessoa. "
            "A minha informação é orientativa e não substitui aconselhamento profissional.\n\n"
            "Ajudo-te com os trâmites sociais em Espanha: "
            "rendimento mínimo, inscrição, cartão de saúde, NIE e mais.\n\n"
            "🗣 Podes *enviar-me um áudio* ou *escrever* a tua pergunta.\n"
            "🌍 Falo espanhol, francês, inglês, português, romeno, catalão, chinês e árabe.\n"
            "🔒 Gratuito e confidencial.\n\n"
            f"📋 Info legal: {LEGAL_PAGE_BASE}?lang=pt"
        ),
        "speech": "Ninguém deveria ficar sozinho perante um trâmite. Sou Clara, uma inteligência artificial que te ouve. Conta-me, no teu idioma.",
        "buttons": [
            {"id": "btn_imv", "title": "O que é o IMV?"},
            {"id": "btn_empadronamiento", "title": "Inscrição"},
            {"id": "btn_salud", "title": "Cartão de saúde"},
        ],
    },
    "ro": {
        "text": (
            "👋 *Bună, sunt Clara.*\n\n"
            "🤖 Sunt o inteligență artificială, nu o persoană. "
            "Informațiile mele sunt orientative și nu înlocuiesc consilierea profesională.\n\n"
            "Te ajut cu procedurile sociale din Spania: "
            "venitul minim, înregistrarea, cardul de sănătate, NIE și altele.\n\n"
            "🗣 Poți să *trimiți un mesaj vocal* sau să *scrii* întrebarea ta.\n"
            "🌍 Vorbesc spaniolă, franceză, engleză, portugheză, română, catalană, chineză și arabă.\n"
            "🔒 Gratuit și confidențial.\n\n"
            f"📋 Info legale: {LEGAL_PAGE_BASE}?lang=ro"
        ),
        "speech": "Nimeni nu ar trebui să fie singur în fața unei proceduri. Sunt Clara, o inteligență artificială care te ascultă. Spune-mi, în limba ta.",
        "buttons": [
            {"id": "btn_imv", "title": "Ce este IMV?"},
            {"id": "btn_empadronamiento", "title": "Înregistrare"},
            {"id": "btn_salud", "title": "Card de sănătate"},
        ],
    },
    "ca": {
        "text": (
            "👋 *Hola, soc la Clara.*\n\n"
            "🤖 Soc una intel·ligència artificial, no una persona. "
            "La meva informació és orientativa i no substitueix l'assessorament professional.\n\n"
            "T'ajudo amb tràmits socials a Espanya: "
            "IMV, empadronament, targeta sanitària, NIE i més.\n\n"
            "🗣 Pots *enviar-me un àudio* o *escriure* la teva pregunta.\n"
            "🌍 Parlo castellà, francès, anglès, portuguès, romanès, català, xinès i àrab.\n"
            "🔒 Gratuït i confidencial.\n\n"
            f"📋 Info legal: {LEGAL_PAGE_BASE}?lang=ca"
        ),
        "speech": "Ningú hauria de quedar-se sol davant un tràmit. Soc Clara, una intel·ligència artificial que t'escolta. Explica'm, en el teu idioma.",
        "buttons": [
            {"id": "btn_imv", "title": "Què és l'IMV?"},
            {"id": "btn_empadronamiento", "title": "Empadronament"},
            {"id": "btn_salud", "title": "Targeta sanitària"},
        ],
    },
    "zh": {
        "text": (
            "👋 *你好，我是Clara。*\n\n"
            "🤖 我是人工智能，不是真人。"
            "我提供的信息仅供参考，不能替代专业建议。\n\n"
            "我帮助你办理西班牙的社会事务：最低收入、登记注册、医疗卡、NIE等。\n\n"
            "🗣 你可以*发送语音*或*输入文字*提问。\n"
            "🌍 我会说西班牙语、法语、英语、葡萄牙语、罗马尼亚语、加泰罗尼亚语、中文和阿拉伯语。\n"
            "🔒 免费且保密。\n\n"
            f"📋 法律信息: {LEGAL_PAGE_BASE}?lang=zh"
        ),
        "speech": "没有人应该独自面对一项手续。我是Clara，一个倾听你的人工智能。告诉我，用你的语言。",
        "buttons": [
            {"id": "btn_imv", "title": "什么是IMV？"},
            {"id": "btn_empadronamiento", "title": "居民登记"},
            {"id": "btn_salud", "title": "医疗卡"},
        ],
    },
    "ar": {
        "text": (
            "👋 *مرحبا، أنا كلارا.*\n\n"
            "🤖 أنا ذكاء اصطناعي، لست شخصاً حقيقياً. "
            "معلوماتي إرشادية ولا تحل محل الاستشارة المهنية.\n\n"
            "أساعدك في الإجراءات الاجتماعية في إسبانيا: "
            "الحد الأدنى للدخل، التسجيل البلدي، البطاقة الصحية، NIE والمزيد.\n\n"
            "🗣 يمكنك *إرسال صوت* أو *كتابة* سؤالك.\n"
            "🌍 أتحدث الإسبانية والفرنسية والإنجليزية والبرتغالية والرومانية والكتالونية والصينية والعربية.\n"
            "🔒 مجاني وسري.\n\n"
            f"📋 المعلومات القانونية: {LEGAL_PAGE_BASE}?lang=ar"
        ),
        "speech": "لا أحد يجب أن يواجه إجراء وحده. أنا كلارا، ذكاء اصطناعي يسمعك. أخبرني، بلغتك.",
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
    to_number = _normalize_mx_number(to_number)
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


GOODBYE = {
    "es": f"Parece que ya no estas. No guardamos ningun dato tuyo, tu privacidad es lo primero. Si vuelves a necesitar ayuda, aqui me tienes. Cuidate mucho!\n\n📋 Info legal y privacidad: {LEGAL_PAGE_BASE}?lang=es",
    "en": f"It seems you've left. We don't store any of your data — your privacy comes first. If you need help again, I'll be here. Take care!\n\n📋 Legal info & privacy: {LEGAL_PAGE_BASE}?lang=en",
    "fr": f"Il semble que tu sois parti. Nous ne conservons aucune de tes donnees, ta vie privee est notre priorite. Si tu as encore besoin d'aide, je suis la. Prends soin de toi!\n\n📋 Infos legales et confidentialite: {LEGAL_PAGE_BASE}?lang=fr",
    "pt": f"Parece que ja foste. Nao guardamos nenhum dado teu, a tua privacidade e o mais importante. Se voltares a precisar de ajuda, estou aqui. Cuida-te!\n\n📋 Info legal e privacidade: {LEGAL_PAGE_BASE}?lang=pt",
    "ro": f"Se pare ca ai plecat. Nu stocam niciun fel de date ale tale, confidentialitatea ta este prioritara. Daca ai nevoie de ajutor din nou, sunt aici. Ai grija de tine!\n\n📋 Info legale si confidentialitate: {LEGAL_PAGE_BASE}?lang=ro",
    "ca": f"Sembla que ja no hi ets. No guardem cap dada teva, la teva privacitat es el primer. Si tornes a necessitar ajuda, aqui em tens. Cuida't molt!\n\n📋 Info legal i privacitat: {LEGAL_PAGE_BASE}?lang=ca",
    "zh": f"看起来你已经离开了。我们不保存你的任何数据，你的隐私是第一位的。如果你再次需要帮助，我在这里。保重！\n\n📋 法律信息与隐私: {LEGAL_PAGE_BASE}?lang=zh",
    "ar": f"يبدو أنك غادرت. لا نحتفظ بأي من بياناتك، خصوصيتك هي الأولوية. إذا احتجت المساعدة مرة أخرى، أنا هنا. اعتنِ بنفسك!\n\n📋 المعلومات القانونية والخصوصية: {LEGAL_PAGE_BASE}?lang=ar",
}

GOODBYE_SPEECH = {
    "es": "Parece que ya no estas. No guardamos ningun dato tuyo. Si vuelves a necesitar ayuda, aqui me tienes. Cuidate mucho.",
    "en": "It seems you've left. We don't store any of your data. If you need help again, I'll be here. Take care.",
    "fr": "Il semble que tu sois parti. Nous ne conservons aucune de tes donnees. Si tu as encore besoin d'aide, je suis la. Prends soin de toi.",
    "pt": "Parece que ja foste. Nao guardamos nenhum dado teu. Se voltares a precisar de ajuda, estou aqui. Cuida-te.",
    "ro": "Se pare ca ai plecat. Nu stocam niciun fel de date ale tale. Daca ai nevoie de ajutor din nou, sunt aici. Ai grija de tine.",
    "ca": "Sembla que ja no hi ets. No guardem cap dada teva. Si tornes a necessitar ajuda, aqui em tens. Cuida't molt.",
    "zh": "看起来你已经离开了。我们不保存你的任何数据。如果你再次需要帮助，我在这里。保重。",
    "ar": "يبدو أنك غادرت. لا نحتفظ بأي من بياناتك. إذا احتجت المساعدة مرة أخرى، أنا هنا. اعتنِ بنفسك.",
}


def send_goodbye(to_number: str, language: str = "es") -> bool:
    """Send goodbye message after prolonged inactivity: text + audio in background."""
    import threading
    to_number = _normalize_mx_number(to_number)
    text = GOODBYE.get(language, GOODBYE["es"])

    # 1. Send goodbye text IMMEDIATELY
    try:
        payload = {
            "messaging_product": "whatsapp",
            "to": to_number,
            "type": "text",
            "text": {"body": text},
        }
        resp = requests.post(_url(), json=payload, headers=_headers(), timeout=10)
        resp.raise_for_status()
    except Exception as e:
        log_error("send_goodbye_text", str(e))
        return False

    # 2. Send goodbye audio in BACKGROUND
    def _send_goodbye_audio():
        try:
            from src.core.skills.tts import text_to_audio
            speech = GOODBYE_SPEECH.get(language, GOODBYE_SPEECH["es"])
            audio_url = text_to_audio(speech, language)
            if audio_url:
                send_audio_only(to_number, audio_url)
        except Exception as e:
            log_error("send_goodbye_audio", str(e))

    t = threading.Thread(target=_send_goodbye_audio, daemon=True)
    t.start()
    return True


def send_followup(to_number: str, language: str = "es") -> bool:
    """Send follow-up after inactivity: buttons first, audio in background."""
    import threading
    to_number = _normalize_mx_number(to_number)
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
