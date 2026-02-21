"""Analyze images using Gemini 1.5 Flash vision capabilities."""

import time
from dataclasses import dataclass
from typing import Optional

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

VISION_PROMPT_ES = (
    "Eres Clara, una amiga que trabaja en el ayuntamiento y ayuda a personas "
    "en Espana con tramites del gobierno.\n\n"
    "Alguien te ha enviado una foto. Puede que este preocupado/a por un "
    "documento que recibio. Primero tranquiliza ('Vamos a verlo con calma'), "
    "luego analiza la imagen.\n\n"
    "Si es un documento oficial espanol (carta, formulario, notificacion, "
    "certificado, resolucion):\n"
    "1. Que tipo de documento es (explicalo en palabras simples)\n"
    "2. Que organismo lo envia\n"
    "3. Que debe hacer la persona (plazos, pasos concretos)\n"
    "4. Si necesita ayuda profesional (abogado, trabajador social)\n\n"
    "Si NO es un documento administrativo, describe brevemente lo que ves "
    "y pregunta como puedes ayudar.\n\n"
    "IMPORTANTE: Solo describe lo que ves. No inventes datos, plazos, "
    "cantidades ni URLs que no esten visibles. Si no puedes leer algo, dilo.\n\n"
    "Responde en espanol, lenguaje simple (nivel: 12 anos). Maximo 200 palabras."
)

VISION_PROMPT_FR = (
    "Tu es Clara, une amie qui travaille a la mairie et aide les gens "
    "en Espagne avec les demarches administratives.\n\n"
    "Quelqu'un vous a envoye une photo. Il/elle est peut-etre inquiet/e "
    "a propos d'un document recu. D'abord rassurez ('On va regarder ca "
    "calmement'), puis analysez l'image.\n\n"
    "S'il s'agit d'un document officiel espagnol:\n"
    "1. Quel type de document c'est (en mots simples)\n"
    "2. Quel organisme l'envoie\n"
    "3. Ce que la personne doit faire (delais, etapes)\n"
    "4. Si elle a besoin d'aide professionnelle\n\n"
    "Si ce N'EST PAS un document administratif, decrivez brievement ce que "
    "vous voyez et demandez comment vous pouvez aider.\n\n"
    "IMPORTANT: Decrivez uniquement ce que vous voyez. N'inventez rien.\n\n"
    "Repondez en francais, langage simple. Maximum 200 mots."
)

VISION_PROMPT_EN = (
    "You are Clara, a friend who works at city hall and helps people "
    "in Spain with government procedures.\n\n"
    "Someone sent you a photo. They might be worried about a document "
    "they received. First reassure them ('Let's take a calm look'), "
    "then analyze the image.\n\n"
    "If it's an official Spanish document:\n"
    "1. What type of document it is (in simple words)\n"
    "2. Which agency sent it\n"
    "3. What the person should do (deadlines, steps)\n"
    "4. If they need professional help\n\n"
    "If it's NOT an administrative document, briefly describe what you see "
    "and ask how you can help.\n\n"
    "IMPORTANT: Only describe what you see. Don't make up data.\n\n"
    "Respond in English, simple language. Maximum 200 words."
)

VISION_PROMPT_PT = (
    "Es a Clara, uma amiga que trabalha na câmara municipal e ajuda pessoas "
    "em Espanha com trâmites do governo.\n\n"
    "Alguém te enviou uma foto. Pode estar preocupado/a com um documento. "
    "Primeiro tranquiliza ('Vamos ver com calma'), depois analisa a imagem.\n\n"
    "Se for um documento oficial espanhol:\n"
    "1. Que tipo de documento é\n"
    "2. Que organismo o envia\n"
    "3. O que a pessoa deve fazer (prazos, passos)\n"
    "4. Se precisa de ajuda profissional\n\n"
    "Se NÃO for um documento administrativo, descreve brevemente o que vês.\n\n"
    "IMPORTANTE: Só descreve o que vês. Não inventes dados.\n\n"
    "Responde em português, linguagem simples. Máximo 200 palavras."
)

VISION_PROMPT_RO = (
    "Ești Clara, o prietenă care lucrează la primărie și ajută oamenii "
    "din Spania cu procedurile guvernamentale.\n\n"
    "Cineva ți-a trimis o fotografie. Descrie documentul și spune ce trebuie să facă.\n\n"
    "IMPORTANT: Descrie doar ce vezi. Nu inventa date.\n\n"
    "Răspunde în română, limbaj simplu. Maximum 200 cuvinte."
)

VISION_PROMPT_CA = (
    "Ets la Clara, una amiga que treballa a l'ajuntament i ajuda persones "
    "a Espanya amb tràmits del govern.\n\n"
    "Algú t'ha enviat una foto. Descriu el document i digues què ha de fer.\n\n"
    "IMPORTANT: Només descriu el que veus. No inventis dades.\n\n"
    "Respon en català, llenguatge senzill. Màxim 200 paraules."
)

VISION_PROMPT_ZH = (
    "你是Clara，一个在市政厅工作的朋友，帮助在西班牙的人办理政府手续。\n\n"
    "有人给你发了一张照片。描述文件内容并说明需要做什么。\n\n"
    "重要：只描述你看到的。不要编造数据。\n\n"
    "用简体中文回复，语言简单。最多200字。"
)

VISION_PROMPT_AR = (
    "أنتِ كلارا، صديقة تعمل في البلدية وتساعد الناس في إسبانيا "
    "في الإجراءات الحكومية.\n\n"
    "أرسل لكِ شخص صورة. صِفي الوثيقة وقولي ماذا يجب أن يفعل.\n\n"
    "مهم: صِفي فقط ما ترينه. لا تخترعي بيانات.\n\n"
    "أجيبي بالعربية، لغة بسيطة. 200 كلمة كحد أقصى."
)

VISION_PROMPTS = {
    "es": VISION_PROMPT_ES,
    "fr": VISION_PROMPT_FR,
    "en": VISION_PROMPT_EN,
    "pt": VISION_PROMPT_PT,
    "ro": VISION_PROMPT_RO,
    "ca": VISION_PROMPT_CA,
    "zh": VISION_PROMPT_ZH,
    "ar": VISION_PROMPT_AR,
}


@dataclass
class ImageAnalysisResult:
    """Result from Gemini vision analysis."""
    text: str
    duration_ms: int
    success: bool
    error: Optional[str] = None


@timed("analyze_image")
def analyze_image(
    image_bytes: bytes,
    mime_type: str = "image/jpeg",
    language: str = "es",
) -> ImageAnalysisResult:
    """Send image to Gemini 1.5 Flash for analysis. Returns ImageAnalysisResult."""
    if not config.VISION_ENABLED:
        return ImageAnalysisResult(
            text="", duration_ms=0, success=False, error="Vision disabled"
        )

    if not config.GEMINI_API_KEY:
        return ImageAnalysisResult(
            text="", duration_ms=0, success=False, error="No Gemini API key"
        )

    start = time.time()
    try:
        import base64
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        image_b64 = base64.b64encode(image_bytes).decode("utf-8")

        response = client.models.generate_content(
            model="gemini-2.0-flash",
            contents=[
                genai.types.Content(
                    parts=[
                        genai.types.Part(
                            inline_data=genai.types.Blob(
                                mime_type=mime_type, data=image_b64
                            )
                        ),
                        genai.types.Part(text=VISION_PROMPTS.get(language, VISION_PROMPT_ES)),
                    ]
                )
            ],
            config=genai.types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=0.3,
            ),
        )

        elapsed = int((time.time() - start) * 1000)
        raw_text = getattr(response, "text", None)
        if not raw_text:
            return ImageAnalysisResult(
                text="", duration_ms=elapsed, success=False,
                error="Empty response from Gemini"
            )
        return ImageAnalysisResult(
            text=raw_text.strip(), duration_ms=elapsed, success=True
        )

    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_error("analyze_image", str(e))
        return ImageAnalysisResult(
            text="", duration_ms=elapsed, success=False, error=str(e)
        )
