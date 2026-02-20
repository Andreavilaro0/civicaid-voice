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
    "documento que recibio. Analiza la imagen con calma.\n\n"
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
    "Quelqu'un t'a envoye une photo. Il/elle est peut-etre inquiet/e "
    "a propos d'un document recu. Analyse l'image calmement.\n\n"
    "S'il s'agit d'un document officiel espagnol:\n"
    "1. Quel type de document c'est (en mots simples)\n"
    "2. Quel organisme l'envoie\n"
    "3. Ce que la personne doit faire (delais, etapes)\n"
    "4. Si elle a besoin d'aide professionnelle\n\n"
    "Si ce N'EST PAS un document administratif, decris brievement ce que "
    "tu vois et demande comment tu peux aider.\n\n"
    "IMPORTANT: Decris uniquement ce que tu vois. N'invente rien.\n\n"
    "Reponds en francais, langage simple. Maximum 200 mots."
)

VISION_PROMPTS = {
    "es": VISION_PROMPT_ES,
    "fr": VISION_PROMPT_FR,
    "en": VISION_PROMPT_ES,  # fallback to ES for now
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
            model="gemini-2.5-flash",
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
