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
    "fallback_generic": {
        "es": "Ahora mismo puedo ayudarte con el Ingreso Mínimo Vital, empadronamiento y tarjeta sanitaria. ¿Sobre qué te gustaría saber?",
        "fr": "Je peux vous aider avec l'Ingreso Mínimo Vital, l'empadronamiento et la tarjeta sanitaria. Quel sujet vous intéresse ?",
        "en": "I can help you with the Ingreso Mínimo Vital, empadronamiento, and tarjeta sanitaria. What would you like to know about?",
    },
    "whisper_fail": {
        "es": "No pude entender tu audio. ¿Podrías escribir tu pregunta?",
        "fr": "Je n'ai pas pu comprendre votre audio. Pourriez-vous écrire votre question ?",
        "en": "I couldn't understand your audio. Could you type your question?",
    },
    "llm_fail": {
        "es": "Hubo un problema al procesar tu consulta. Prueba de nuevo en unos segundos, o consulta directamente en:\n- IMV: 900 20 22 22\n- Empadronamiento: 010\n- Tarjeta sanitaria: 900 102 112",
        "fr": "Un problème est survenu. Réessayez dans quelques secondes, ou appelez directement :\n- IMV : 900 20 22 22\n- Empadronamiento : 010\n- Carte sanitaire : 900 102 112",
        "en": "There was a problem processing your query. Try again in a few seconds, or call directly:\n- IMV: 900 20 22 22\n- Registration: 010\n- Health card: 900 102 112",
    },
}


def get_template(template_key: str, language: str = "es") -> str:
    templates = TEMPLATES.get(template_key, {})
    return templates.get(language, templates.get("es", ""))
