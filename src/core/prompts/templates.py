"""Response templates by type: greeting, tramite, error, fallback."""

_GREETING_WORDS = {
    # Spanish
    "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
    "que tal", "ey",
    # French
    "bonjour", "salut", "bonsoir",
    # English
    "hello", "hi", "hey", "help", "start",
    # Portuguese
    "ola", "oi", "bom dia", "boa tarde", "boa noite",
    # Arabic (transliterated)
    "salam", "marhaba", "ahlan",
    # Generic
    "join", "empezar", "ayuda",
}


def is_greeting(text: str) -> bool:
    """Check if message is a greeting/first contact."""
    words = text.lower().strip().split()
    if len(words) <= 4:
        return any(w in _GREETING_WORDS for w in words) or text.lower().strip() in _GREETING_WORDS
    return False


TEMPLATES = {
    "ack_greeting": {
        "es": "Hola! Soy Clara. Estoy aqui para echarte una mano con tramites y ayudas. Cuentame, que necesitas?",
        "fr": "Bonjour ! Je suis Clara. Je suis la pour vous aider avec vos demarches. Dites-moi, de quoi avez-vous besoin ?",
        "en": "Hi! I'm Clara. I'm here to help you with government procedures and benefits. What do you need?",
        "pt": "Ola! Sou a Clara. Estou aqui para te ajudar com processos e ajudas. Conta-me, do que precisas?",
        "ar": "اهلا! انا كلارا. انا هنا لمساعدتك في المعاملات والمساعدات. بماذا تحتاج مساعدة؟",
    },
    "ack_text": {
        "es": "Dame un momento, estoy buscando esa informacion.",
        "fr": "Un instant, je cherche cette information.",
        "en": "One moment, I'm looking into this.",
        "pt": "Um momento, estou a procurar essa informacao.",
        "ar": "لحظة، أبحث عن هذه المعلومات.",
    },
    "ack_audio": {
        "es": "Estoy escuchando tu mensaje, un momento.",
        "fr": "J'ecoute votre message, un instant.",
        "en": "Listening to your message, one moment.",
        "pt": "Estou a ouvir a tua mensagem, um momento.",
        "ar": "أستمع لرسالتك، لحظة من فضلك.",
    },
    "ack_image": {
        "es": "Estoy mirando tu imagen, dame un momento.",
        "fr": "Je regarde votre image, un instant.",
        "en": "Looking at your image, one moment.",
        "pt": "Estou a ver a tua imagem, um momento.",
        "ar": "أنظر إلى صورتك، لحظة من فضلك.",
    },
    "vision_fail": {
        "es": "No he podido ver bien la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves y te ayudo.",
        "fr": "Je n'ai pas pu bien voir l'image. Vous pouvez la renvoyer, ou si vous preferez, decrivez-moi ce que vous voyez.",
        "en": "I couldn't see the image clearly. You can try sending it again, or describe what you see and I'll help.",
    },
    "fallback_generic": {
        "es": "Estoy aqui para ayudarte con tramites, ayudas y procesos del gobierno espanol. Sobre que necesitas informacion?",
        "fr": "Je suis la pour vous aider avec les demarches et aides du gouvernement espagnol. De quoi avez-vous besoin ?",
        "en": "I'm here to help you with procedures and benefits from the Spanish government. What do you need information about?",
        "pt": "Estou aqui para te ajudar com processos e ajudas do governo espanhol. Sobre o que precisas de informacao?",
        "ar": "أنا هنا لمساعدتك في المعاملات والمساعدات الحكومية الإسبانية. بماذا تحتاج مساعدة؟",
    },
    "whisper_fail": {
        "es": "No he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta.",
        "fr": "Je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou si vous preferez, ecrivez votre question.",
        "en": "I couldn't hear your audio clearly. You can try again, or if you prefer, type your question.",
    },
    "llm_fail": {
        "es": "Ha habido un problema por mi parte. Puedes intentar de nuevo en unos segundos, o si lo prefieres, consulta en administracion.gob.es o escribe al 060.",
        "fr": "Il y a eu un probleme de mon cote. Reessayez dans quelques secondes, ou consultez administracion.gob.es.",
        "en": "There was a problem on my end. You can try again in a few seconds, or visit administracion.gob.es.",
    },
    "closing": {
        "es": "Si necesitas algo mas, aqui estoy. Mucho animo con tu tramite.",
        "fr": "Si vous avez besoin de quoi que ce soit, je suis la. Bon courage pour vos demarches.",
        "en": "If you need anything else, I'm here. Good luck with your process.",
    },
    "memory_optin_ask": {
        "es": "Para ayudarte mejor, puedo recordar tu consulta. Quieres que recuerde tu tramite? (Si/No)\n\nPuedes decir 'Olvida mis datos' en cualquier momento.",
        "fr": "Pour mieux vous aider, je peux memoriser votre consultation. Voulez-vous que je me souvienne ? (Oui/Non)\n\nVous pouvez dire 'Oublie mes donnees' a tout moment.",
        "en": "To help you better, I can remember your case. Would you like me to remember? (Yes/No)\n\nYou can say 'Forget my data' at any time.",
    },
    "memory_optin_confirmed": {
        "es": "Perfecto, recordare tu consulta para ayudarte mejor. Puedes decir 'Olvida mis datos' cuando quieras.",
        "fr": "Parfait, je me souviendrai de votre consultation. Dites 'Oublie mes donnees' quand vous voulez.",
        "en": "Great, I'll remember your case. Say 'Forget my data' whenever you want.",
    },
    "memory_optin_declined": {
        "es": "Entendido, no guardare datos. Cada mensaje sera independiente.",
        "fr": "Compris, je ne garderai pas de donnees. Chaque message sera independant.",
        "en": "Got it, I won't store data. Each message will be independent.",
    },
    "memory_forgotten": {
        "es": "Tus datos han sido eliminados. Si necesitas ayuda, escribe cuando quieras.",
        "fr": "Vos donnees ont ete supprimees. Si vous avez besoin d'aide, ecrivez quand vous voulez.",
        "en": "Your data has been deleted. If you need help, write anytime.",
    },
}


def get_template(template_key: str, language: str = "es") -> str:
    templates = TEMPLATES.get(template_key, {})
    return templates.get(language, templates.get("es", ""))
