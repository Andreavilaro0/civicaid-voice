"""Response templates by type: greeting, tramite, error, fallback."""

_GREETING_WORDS = {
    # Spanish
    "hola", "buenas", "buenos dias", "buenas tardes", "buenas noches",
    "que tal", "ey",
    # French
    "bonjour", "salut", "bonsoir",
    # English
    "hello", "hi", "hey", "help", "start",
    # Portuguese (with and without accents)
    "ola", "olá", "oi", "bom dia", "boa tarde", "boa noite",
    # Romanian (with and without accents)
    "buna", "bună", "buna ziua", "bună ziua", "salut",
    # Catalan
    "bon dia", "bona tarda",
    # Chinese
    "你好", "nihao",
    # Arabic (transliterated + script)
    "salam", "marhaba", "ahlan", "مرحبا", "أهلا", "سلام",
    # Generic
    "join", "empezar", "ayuda",
}


def is_greeting(text: str) -> bool:
    """Check if message is a greeting/first contact."""
    import re
    clean = re.sub(r'[^\w\s]', '', text.lower().strip())
    words = clean.split()
    if len(words) <= 4:
        return any(w in _GREETING_WORDS for w in words) or clean in _GREETING_WORDS
    return False


TEMPLATES = {
    # --- Greetings: Hero arrives, Guide welcomes with warmth ---
    "ack_greeting": {
        "es": "Hola! Soy Clara, encantada de conocerte. Cuentame, en que te puedo echar una mano?",
        "fr": "Bonjour ! Je suis Clara, ravie de vous connaitre. Dites-moi, comment je peux vous aider ?",
        "en": "Hi! I'm Clara, lovely to meet you. Tell me, how can I help?",
        "pt": "Ola! Sou a Clara, prazer em conhecer-te. Conta-me, em que te posso ajudar?",
        "ro": "Buna! Sunt Clara, incantata de cunostinta. Spune-mi, cu ce te pot ajuta?",
        "ca": "Hola! Soc la Clara, encantada de coneixer-te. Digues-me, en que et puc ajudar?",
        "zh": "你好！我是Clara，很高兴认识你。告诉我，我能帮你什么？",
        "ar": "اهلا! انا كلارا، سعيدة بمعرفتك. قولي، كيف أقدر أساعدك؟",
    },
    # --- ACKs: Reassure the hero while searching ---
    "ack_text": {
        "es": "Buena pregunta. Dame un momento que busco la informacion.",
        "fr": "Bonne question. Un instant, je cherche l'information.",
        "en": "Good question. Give me a moment to look into this.",
        "pt": "Boa pergunta. Da-me um momento que procuro a informacao.",
        "ro": "Intrebare buna. Da-mi un moment sa caut informatia.",
        "ca": "Bona pregunta. Dona'm un moment que busco la informacio.",
        "zh": "好问题。请等一下，我查找一下信息。",
        "ar": "سؤال جيد. لحظة، أبحث عن المعلومات.",
    },
    "ack_audio": {
        "es": "Te escucho. Dame un momento.",
        "fr": "Je vous ecoute. Un instant.",
        "en": "I hear you. Give me a moment.",
        "pt": "Estou a ouvir-te. Da-me um momento.",
        "ro": "Te aud. Da-mi un moment.",
        "ca": "T'escolto. Dona'm un moment.",
        "zh": "我听到了。请等一下。",
        "ar": "أسمعك. لحظة من فضلك.",
    },
    "ack_image": {
        "es": "Voy a mirar tu documento. Dame un segundo.",
        "fr": "Je regarde votre document. Un instant.",
        "en": "Let me look at your document. One second.",
        "pt": "Vou ver o teu documento. Da-me um segundo.",
        "ro": "Ma uit la documentul tau. O secunda.",
        "ca": "Vaig a mirar el teu document. Dona'm un segon.",
        "zh": "让我看看你的文件。请等一下。",
        "ar": "سأنظر في وثيقتك. لحظة من فضلك.",
    },
    # --- Errors: Own the failure, reassure the hero, offer alternatives ---
    "vision_fail": {
        "es": "No te preocupes, no he podido ver bien la imagen. Puedes intentar enviarla de nuevo, o si prefieres, describeme lo que ves y te ayudo igual.",
        "fr": "Ne vous inquietez pas, je n'ai pas pu bien voir l'image. Vous pouvez la renvoyer, ou decrivez-moi ce que vous voyez et je vous aide.",
        "en": "Don't worry, I couldn't see the image clearly. You can try sending it again, or describe what you see and I'll help.",
        "pt": "Nao te preocupes, nao consegui ver bem a imagem. Podes tentar enviar de novo, ou descreve-me o que ves e eu ajudo-te.",
        "ro": "Nu-ti face griji, nu am putut vedea bine imaginea. Poti incerca din nou, sau descrie-mi ce vezi si te ajut.",
        "ca": "No et preocupis, no he pogut veure be la imatge. Pots intentar enviar-la de nou, o descriu-me el que veus i t'ajudo.",
        "zh": "别担心，我没有看清图片。你可以再发一次，或者描述你看到的内容，我来帮你。",
        "ar": "لا تقلق، لم أستطع رؤية الصورة بوضوح. يمكنك إرسالها مرة أخرى، أو صف لي ما تراه وسأساعدك.",
    },
    "fallback_generic": {
        "es": "Estoy aqui para echarte una mano. Puedo ayudarte con tramites, ayudas, papeles del gobierno... lo que necesites. Por donde quieres empezar?",
        "fr": "Je suis la pour vous aider. Demarches, aides, documents du gouvernement... ce que vous voulez. Par ou voulez-vous commencer ?",
        "en": "I'm here to help. Government procedures, benefits, paperwork... whatever you need. Where would you like to start?",
        "pt": "Estou aqui para te ajudar. Processos, ajudas, papeis do governo... o que precisares. Por onde queres comecar?",
        "ro": "Sunt aici sa te ajut. Proceduri, ajutoare, acte de la stat... ce ai nevoie. De unde vrei sa incepem?",
        "ca": "Soc aqui per ajudar-te. Tramits, ajudes, papers del govern... el que necessitis. Per on vols comencar?",
        "zh": "我在这里帮你。政府手续、补助、证件……你需要什么都可以问。你想从哪里开始？",
        "ar": "أنا هنا لمساعدتك. معاملات، مساعدات، أوراق حكومية... ما تحتاجه. من أين تريد أن نبدأ؟",
    },
    "whisper_fail": {
        "es": "Perdona, no he podido escuchar bien tu audio. Puedes intentar de nuevo, o si prefieres, escribeme tu pregunta y te ayudo.",
        "fr": "Pardon, je n'ai pas pu bien entendre votre audio. Vous pouvez reessayer, ou ecrivez-moi votre question.",
        "en": "Sorry, I couldn't hear your audio clearly. You can try again, or type your question and I'll help.",
        "pt": "Desculpa, nao consegui ouvir bem o teu audio. Podes tentar de novo, ou escreve-me a tua pergunta.",
        "ro": "Scuze, nu am putut auzi bine mesajul tau vocal. Poti incerca din nou, sau scrie-mi intrebarea ta.",
        "ca": "Perdona, no he pogut escoltar be el teu audio. Pots intentar-ho de nou, o si prefereixes, escriu-me la teva pregunta.",
        "zh": "抱歉，我没有听清你的语音。你可以再试一次，或者把问题写给我。",
        "ar": "عذراً، لم أستطع سماع رسالتك الصوتية بوضوح. يمكنك المحاولة مرة أخرى، أو اكتب لي سؤالك.",
    },
    "llm_fail": {
        "es": "Perdoname, ha habido un fallo por mi parte. Puedes intentar de nuevo en unos segundos. Y si es urgente, llama al 060 o entra en administracion.gob.es. Yo sigo aqui.",
        "fr": "Pardon, il y a eu un souci de mon cote. Reessayez dans quelques secondes. Si c'est urgent, consultez administracion.gob.es ou appelez le 060.",
        "en": "Sorry, something went wrong on my end. You can try again in a few seconds. If it's urgent, call 060 or visit administracion.gob.es. I'm still here.",
        "pt": "Desculpa, houve um problema do meu lado. Podes tentar de novo em alguns segundos. Se for urgente, liga para o 060 ou consulta administracion.gob.es.",
        "ro": "Scuze, a aparut o problema din partea mea. Poti incerca din nou in cateva secunde. Daca e urgent, suna la 060 sau viziteaza administracion.gob.es.",
        "ca": "Perdona'm, hi ha hagut un error per la meva part. Pots intentar-ho de nou en uns segons. Si es urgent, truca al 060 o entra a administracion.gob.es.",
        "zh": "抱歉，我这边出了点问题。你可以几秒后再试。如果紧急，请拨打060或访问 administracion.gob.es。",
        "ar": "عذراً، حدثت مشكلة من جانبي. يمكنك المحاولة مرة أخرى بعد ثوانٍ. إذا كان الأمر عاجلاً، اتصل بـ 060 أو زر administracion.gob.es.",
    },
    # --- Suggested questions: When user seems lost ---
    "suggest_questions": {
        "es": "Puedo ayudarte con cosas como:\n- Como pido el *Ingreso Minimo Vital*?\n- Que necesito para *empadronarme*?\n- Como saco la *tarjeta sanitaria*?\n- Como renuevo mi *NIE*?\n\nPreguntame lo que necesites.",
        "fr": "Je peux vous aider avec des questions comme :\n- Comment demander le *Revenu Minimum Vital* ?\n- Comment m'*inscrire au padron* ?\n- Comment obtenir la *carte sanitaire* ?\n- Comment renouveler mon *NIE* ?\n\nDemandez-moi ce que vous voulez.",
        "en": "I can help with questions like:\n- How do I apply for the *Minimum Living Income*?\n- How do I *register at the town hall*?\n- How do I get my *health card*?\n- How do I renew my *NIE*?\n\nAsk me anything you need.",
        "pt": "Posso ajudar-te com coisas como:\n- Como peco o *Rendimento Minimo*?\n- Como me *empadrono*?\n- Como tiro o *cartao de saude*?\n- Como renovo o meu *NIE*?\n\nPergunta-me o que precisares.",
        "ro": "Te pot ajuta cu lucruri ca:\n- Cum solicit *Venitul Minim*?\n- Cum ma *inregistrez la primarie*?\n- Cum obtin *cardul sanitar*?\n- Cum imi reinnoiesc *NIE-ul*?\n\nIntreaba-ma ce ai nevoie.",
        "ca": "Puc ajudar-te amb coses com:\n- Com demano el *Ingrés Mínim Vital*?\n- Com m'*empadrono*?\n- Com trec la *targeta sanitaria*?\n- Com renovo el meu *NIE*?\n\nPregunta'm el que necessitis.",
        "zh": "我可以帮你解答这些问题：\n- 如何申请*最低生活保障*？\n- 如何*登记住址*？\n- 如何办理*医疗卡*？\n- 如何更新*NIE*？\n\n问我任何你需要的。",
        "ar": "أقدر أساعدك في أشياء مثل:\n- كيف أطلب *الحد الأدنى للدخل*؟\n- كيف *أسجل في البلدية*؟\n- كيف أحصل على *البطاقة الصحية*؟\n- كيف أجدد *NIE*؟\n\nاسألني ما تحتاج.",
    },
    # --- Privacy notice: Proactive data reassurance ---
    "privacy_notice": {
        "es": "Por cierto, no guardo ningun dato tuyo. Cada conversacion empieza de cero. Tu privacidad es lo primero.",
        "fr": "Au fait, je ne garde aucune donnee. Chaque conversation repart de zero. Votre vie privee est prioritaire.",
        "en": "By the way, I don't store any of your data. Each conversation starts fresh. Your privacy comes first.",
        "pt": "Ja agora, nao guardo nenhum dado teu. Cada conversa comeca de zero. A tua privacidade e o mais importante.",
        "ro": "Apropo, nu pastrez niciun dat al tau. Fiecare conversatie incepe de la zero. Confidentialitatea ta e pe primul loc.",
        "ca": "Per cert, no guardo cap dada teva. Cada conversa comenca de zero. La teva privacitat es el primer.",
        "zh": "顺便说一下，我不保存你的任何数据。每次对话都从零开始。你的隐私是最重要的。",
        "ar": "بالمناسبة، أنا لا أحتفظ بأي بيانات لك. كل محادثة تبدأ من الصفر. خصوصيتك أولاً.",
    },
    # --- Closing: Celebrate the hero's journey ---
    "closing": {
        "es": "Ya tienes lo que necesitas. Si te surge otra duda, aqui estoy. Mucho animo, lo vas a sacar adelante.",
        "fr": "Vous avez ce qu'il faut. Si une autre question se pose, je suis la. Bon courage, vous allez y arriver.",
        "en": "You've got what you need. If anything else comes up, I'm here. You've got this.",
        "pt": "Ja tens o que precisas. Se surgir outra duvida, estou aqui. Muita forca, vais conseguir.",
        "ro": "Ai tot ce ai nevoie. Daca apare alta intrebare, sunt aici. Mult curaj, o sa reusesti.",
        "ca": "Ja tens el que necessites. Si et sorgeix un altre dubte, aqui estic. Molt d'anim, ho trauras endavant.",
        "zh": "你已经有了需要的信息。如果还有问题，我在这里。加油，你一定行的。",
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
