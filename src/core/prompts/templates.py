"""Response templates by type: greeting, tramite, error, fallback."""

TEMPLATES = {
    "ack_text": {
        "es": "Un momento, estoy procesando tu mensaje... ⏳",
        "fr": "Un moment, je traite votre message... ⏳",
        "en": "One moment, processing your message... ⏳",
    },
    "ack_audio": {
        "es": "Estoy escuchando tu audio... 🎧",
        "fr": "J'écoute votre audio... 🎧",
        "en": "Listening to your audio... 🎧",
    },
    "ack_image": {
        "es": "Estoy analizando tu imagen... \U0001f4f7",
        "fr": "J'analyse votre image... \U0001f4f7",
        "en": "Analyzing your image... \U0001f4f7",
    },
    "vision_fail": {
        "es": "No pude analizar la imagen. \u00bfPodr\u00edas describir lo que ves o escribir tu pregunta?",
        "fr": "Je n'ai pas pu analyser l'image. Pourriez-vous d\u00e9crire ce que vous voyez ?",
        "en": "I couldn't analyze the image. Could you describe what you see or type your question?",
    },
    "fallback_generic": {
        "es": "Puedo ayudarte con trámites, ayudas y procesos del gobierno español. ¿Sobre qué necesitas información?",
        "fr": "Je peux vous aider avec les démarches, aides et procédures du gouvernement espagnol. De quoi avez-vous besoin ?",
        "en": "I can help you with procedures, benefits, and processes of the Spanish government. What do you need information about?",
    },
    "whisper_fail": {
        "es": "No pude entender tu audio. ¿Podrías escribir tu pregunta?",
        "fr": "Je n'ai pas pu comprendre votre audio. Pourriez-vous écrire votre question ?",
        "en": "I couldn't understand your audio. Could you type your question?",
    },
    "llm_fail": {
        "es": "Hubo un problema al procesar tu consulta. Prueba de nuevo en unos segundos, o consulta directamente en administracion.gob.es o llama al 060.",
        "fr": "Un problème est survenu. Réessayez dans quelques secondes, ou consultez administracion.gob.es ou appelez le 060.",
        "en": "There was a problem processing your query. Try again in a few seconds, or visit administracion.gob.es or call 060.",
    },
    "memory_optin_ask": {
        "es": "Para ayudarte mejor, puedo recordar tu consulta. ¿Quieres que recuerde tu trámite? (Sí/No)\n\nPuedes decir 'Olvida mis datos' en cualquier momento.",
        "fr": "Pour mieux vous aider, je peux mémoriser votre consultation. Voulez-vous que je me souvienne ? (Oui/Non)\n\nVous pouvez dire 'Oublie mes données' à tout moment.",
        "en": "To help you better, I can remember your case. Would you like me to remember? (Yes/No)\n\nYou can say 'Forget my data' at any time.",
    },
    "memory_optin_confirmed": {
        "es": "Perfecto, recordaré tu consulta para ayudarte mejor. Puedes decir 'Olvida mis datos' cuando quieras.",
        "fr": "Parfait, je me souviendrai de votre consultation. Dites 'Oublie mes données' quand vous voulez.",
        "en": "Great, I'll remember your case. Say 'Forget my data' whenever you want.",
    },
    "memory_optin_declined": {
        "es": "Entendido, no guardaré datos. Cada mensaje será independiente.",
        "fr": "Compris, je ne garderai pas de données. Chaque message sera indépendant.",
        "en": "Got it, I won't store data. Each message will be independent.",
    },
    "memory_forgotten": {
        "es": "Tus datos han sido eliminados. Si necesitas ayuda, empieza de nuevo.",
        "fr": "Vos données ont été supprimées. Si vous avez besoin d'aide, recommencez.",
        "en": "Your data has been deleted. If you need help, start over.",
    },
}


def get_template(template_key: str, language: str = "es") -> str:
    templates = TEMPLATES.get(template_key, {})
    return templates.get(language, templates.get("es", ""))
