"""Analyze images using Gemini 1.5 Flash vision capabilities."""

import time
from dataclasses import dataclass
from typing import Optional

from src.core.config import config
from src.utils.logger import log_error
from src.utils.timing import timed

VISION_PROMPT = (
    "Eres Clara, asistente que ayuda a personas vulnerables en Espa\u00f1a con tr\u00e1mites del gobierno.\n"
    "Analiza esta imagen. Si es un documento oficial espa\u00f1ol (carta, formulario, notificaci\u00f3n, "
    "certificado, resoluci\u00f3n), identifica:\n"
    "1. Qu\u00e9 tipo de documento es\n"
    "2. Qu\u00e9 organismo lo env\u00eda\n"
    "3. Qu\u00e9 acci\u00f3n debe tomar la persona (plazos, pasos)\n"
    "4. Si necesita ayuda profesional\n\n"
    "Si NO es un documento administrativo, describe brevemente lo que ves y pregunta "
    "c\u00f3mo puedes ayudar con tr\u00e1mites del gobierno espa\u00f1ol.\n\n"
    "Responde en espa\u00f1ol, lenguaje simple (nivel de comprensi\u00f3n: 12 a\u00f1os). M\u00e1ximo 200 palabras."
)


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
            model="gemini-1.5-flash",
            contents=[
                genai.types.Content(
                    parts=[
                        genai.types.Part(
                            inline_data=genai.types.Blob(
                                mime_type=mime_type, data=image_b64
                            )
                        ),
                        genai.types.Part(text=VISION_PROMPT),
                    ]
                )
            ],
            config=genai.types.GenerateContentConfig(
                max_output_tokens=500,
                temperature=0.3,
            ),
        )

        elapsed = int((time.time() - start) * 1000)
        text = response.text.strip()
        return ImageAnalysisResult(
            text=text, duration_ms=elapsed, success=True
        )

    except Exception as e:
        elapsed = int((time.time() - start) * 1000)
        log_error("analyze_image", str(e))
        return ImageAnalysisResult(
            text="", duration_ms=elapsed, success=False, error=str(e)
        )
