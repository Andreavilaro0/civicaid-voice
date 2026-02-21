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
    # --- Greetings: Hero arrives, Guide welcomes with warmth ---
    "ack_greeting": {
        "es": "Hola! Soy Clara, encantada de conocerte. Cuentame, en que te puedo echar una mano?",
        "fr": "Bonjour ! Je suis Clara, ravie de vous connaitre. Dites-moi, comment je peux vous aider ?",
        "en": "Hi! I'm Clara, lovely to meet you. Tell me, how can I help?",
        "pt": "Ola! Sou a Clara, prazer em conhecer-te. Conta-me, em que te posso ajudar?",
        "ar": "اهلا! انا كلارا، سعيدة بمعرفتك. قولي، كيف أقدر أساعدك؟",
    },
    # --- ACKs: Reassure the hero while searching ---
    "ack_text": {
        "es": "Buena pregunta. Dame un momento que busco la informacion.",
        "fr": "Bonne question. Un instant, je cherche l'information.",
        "en": "Good question. Give me a moment to look into this.",
        "pt": "Boa pergunta. Da-me um momento que procuro a informacao.",
        "ar": "سؤال جيد. لحظة، أبحث عن المعلومات.",
    },
    "ack_audio": {
        "es": "Te escucho. Dame un momento.",
        "fr": "Je vous ecoute. Un instant.",
        "en": "I hear you. Give me a moment.",
        "pt": "Estou a ouvir-te. Da-me um momento.",
        "ar": "أسمعك. لحظة من فضلك.",
    },
    "ack_image": {
        "es": "Voy a mirar tu documento. Dame un segundo.",
        "fr": "Je regarde votre document. Un instant.",
        "en": "Let me look at your document. One second.",
        "pt": "Vou ver o teu documento. Da-me um segundo.",
        "ar": "سأنظر في وثيقتك. لحظة من فضلك.",
    },
    # --- Errors: Own the failure, reassure the hero, offer alternatives ---
    "vision_fail": {
        "es": "No te preocupes, no he podido ver bien la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves y te ayudo igual.",
        "fr": "Ne vous inquietez pas, je n'ai pas pu bien voir l'image. Vous pouvez la renvoyer, ou decrivez-moi ce que vous voyez et je vous aide.",
        "en": "Don't worry, I couldn't see the image clearly. You can try sending it again, or describe what you see and I'll help.",
        "pt": "Nao te preocupes, nao consegui ver bem a imagem. Podes tentar enviar de novo, ou descreve-me o que ves e eu ajudo-te.",
        "ar": "لا تقلق، لم أستطع رؤية الصورة بوضوح. يمكنك إرسالها مرة أخرى، أو صف لي ما تراه وسأساعدك.",
    },
    "fallback_generic": {
        "es": "Estoy aqui para echarte una mano. Puedo ayudarte con tramites, ayudas, papeles del gobierno... lo que necesites. Por donde quieres empezar?",
        "fr": "Je suis la pour vous aider. Demarches, aides, documents du gouvernement... ce que vous voulez. Par ou voulez-vous commencer ?",
        "en": "I'm here to help. Government procedures, benefits, paperwork... whatever you need. Where would you like to start?",
        "pt": "Estou aqui para te ajudar. Processos, ajudas, papeis do governo... o que precisares. Por onde queres comecar?",
        "ar": "أنا هنا لمساعدتك. معاملات، مساعدات، أوراق حكومية... ما تحتاجه. من أين تريد أن نبدأ؟",
    },
    "whisper_fail": {
        "es": "Perdona, no he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta y te ayudo.",
        "fr": "Pardon, je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou ecrivez-moi votre question.",
        "en": "Sorry, I couldn't hear your audio clearly. You can try again, or type your question and I'll help.",
        "pt": "Desculpa, nao consegui ouvir bem o teu audio. Podes tentar de novo, ou escreve-me a tua pergunta.",
        "ar": "عذراً، لم أستطع سماع رسالتك الصوتية بوضوح. يمكنك المحاولة مرة أخرى، أو اكتب لي سؤالك.",
    },
    "llm_fail": {
        "es": "Perdoname, ha habido un fallo por mi parte. Puedes intentar de nuevo en unos segundos. Y si es urgente, llama al 060 o entra en administracion.gob.es. Yo sigo aqui.",
        "fr": "Pardon, il y a eu un souci de mon cote. Reessayez dans quelques secondes. Si c'est urgent, consultez administracion.gob.es ou appelez le 060.",
        "en": "Sorry, something went wrong on my end. You can try again in a few seconds. If it's urgent, call 060 or visit administracion.gob.es. I'm still here.",
        "pt": "Desculpa, houve um problema do meu lado. Podes tentar de novo em alguns segundos. Se for urgente, liga para o 060 ou consulta administracion.gob.es.",
        "ar": "عذراً، حدثت مشكلة من جانبي. يمكنك المحاولة مرة أخرى بعد ثوانٍ. إذا كان الأمر عاجلاً، اتصل بـ 060 أو زر administracion.gob.es.",
    },
    # --- Closing: Celebrate the hero's journey ---
    "closing": {
        "es": "Ya tienes lo que necesitas. Si te surge otra duda, aqui estoy. Mucho animo, lo vas a sacar adelante.",
        "fr": "Vous avez ce qu'il faut. Si une autre question se pose, je suis la. Bon courage, vous allez y arriver.",
        "en": "You've got what you need. If anything else comes up, I'm here. You've got this.",
        "pt": "Ja tens o que precisas. Se surgir outra duvida, estou aqui. Muita forca, vais conseguir.",
        "ar": "لديك ما تحتاجه. إذا ظهر سؤال آخر، أنا هنا. ستنجح في ذلك.",
    },
    # --- Memory: A friend remembering, not a system storing ---
    "memory_optin_ask": {
        "es": "Para no hacerte repetir todo, puedo recordar tu consulta. Quieres que me acuerde? (Si/No)\n\nPuedes decir 'Olvida mis datos' cuando quieras.",
        "fr": "Pour ne pas vous faire tout repeter, je peux me souvenir de votre cas. Voulez-vous ? (Oui/Non)\n\nVous pouvez dire 'Oublie mes donnees' a tout moment.",
        "en": "So you don't have to repeat everything, I can remember your case. Would you like that? (Yes/No)\n\nYou can say 'Forget my data' anytime.",
    },
    "memory_optin_confirmed": {
        "es": "Perfecto, me acuerdo de tu caso. Asi la proxima vez retomamos donde lo dejamos. Di 'Olvida mis datos' cuando quieras.",
        "fr": "Parfait, je me souviens de votre cas. La prochaine fois, on reprend ou on en etait. Dites 'Oublie mes donnees' quand vous voulez.",
        "en": "Great, I'll remember your case. Next time we'll pick up where we left off. Say 'Forget my data' whenever you want.",
    },
    "memory_optin_declined": {
        "es": "Sin problema, no guardo nada. Cada conversacion empieza de cero.",
        "fr": "Pas de souci, je ne garde rien. Chaque conversation repart de zero.",
        "en": "No problem, I won't keep anything. Each conversation starts fresh.",
    },
    "memory_forgotten": {
        "es": "Listo, tus datos han sido borrados. Si necesitas ayuda otra vez, aqui me tienes.",
        "fr": "C'est fait, vos donnees ont ete supprimees. Si vous avez besoin d'aide, je suis la.",
        "en": "Done, your data has been deleted. If you need help again, I'm here.",
    },
}


def get_template(template_key: str, language: str = "es") -> str:
    templates = TEMPLATES.get(template_key, {})
    return templates.get(language, templates.get("es", ""))
