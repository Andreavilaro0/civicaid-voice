#!/usr/bin/env python3
"""Generate photorealistic images using Gemini/Imagen API.

Usage:
    python scripts/media/generate_image.py "prompt text" output.png
    python scripts/media/generate_image.py "prompt text" output.png --model imagen
    python scripts/media/generate_image.py "prompt text" output.png --model flash --aspect 16:9
    python scripts/media/generate_image.py --preset maria    # Use a predefined persona prompt
    python scripts/media/generate_image.py --preset ahmed --output design/mockups/ahmed.png
    python scripts/media/generate_image.py --list-presets    # List all available presets
"""

import argparse
import os
import sys
import time
from pathlib import Path

# --- Clara brand constants for visual consistency ---
CLARA_BLUE = "#1B5E7B"
CLARA_ORANGE = "#D46A1E"
CLARA_GREEN = "#2E7D4F"
CLARA_STYLE_SUFFIX = (
    "Photorealistic, documentary cinematic style. Warm golden lighting. "
    "Shallow depth of field. Color palette includes warm tones with touches "
    f"of blue ({CLARA_BLUE}). Shot at eye level. Intimate, hopeful mood. "
    "No text overlays, no watermarks. 8K quality."
)

# --- Predefined persona/scene presets ---
PRESETS = {
    # --- Persona scenes ---
    "maria": {
        "prompt": (
            "A 58-year-old Moroccan woman named Maria sitting at a kitchen table "
            "in a modest but warm Spanish apartment. She is looking at her smartphone "
            "with a relieved, hopeful expression. A cup of tea is next to her. "
            "Warm golden morning light streams through sheer curtains. "
            "She wears a comfortable sweater. " + CLARA_STYLE_SUFFIX
        ),
        "output": "design/mockups/maria-kitchen.png",
    },
    "ahmed": {
        "prompt": (
            "A 34-year-old Senegalese man named Ahmed sitting on a park bench "
            "in a Spanish city. He is recording a voice message on his phone, "
            "speaking with a focused but calm expression. Green trees and "
            "Mediterranean architecture in the background. Warm afternoon light. "
            "He wears a casual jacket. " + CLARA_STYLE_SUFFIX
        ),
        "output": "design/mockups/ahmed-park.png",
    },
    "fatima": {
        "prompt": (
            "A 42-year-old mother of North African descent, sitting at a dining "
            "table with her two children (ages 8 and 12) beside her. She holds "
            "an official document in one hand and her phone in the other, looking "
            "at the phone with understanding and slight smile. Children lean in "
            "curiously. Warm interior lighting with a family atmosphere. "
            "Spanish apartment interior. " + CLARA_STYLE_SUFFIX
        ),
        "output": "design/mockups/fatima-family.png",
    },
    # --- Product/UI scenes ---
    "hands-phone": {
        "prompt": (
            "Extreme close-up of hands holding a smartphone. The screen shows a "
            "WhatsApp conversation with green message bubbles. The person's thumb "
            "taps a voice message button and begins recording. Warm soft lighting. "
            "Shallow depth of field. The hands belong to a middle-aged person. "
            "Smooth, steady camera angle. " + CLARA_STYLE_SUFFIX
        ),
        "output": "design/mockups/hands-phone-whatsapp.png",
    },
    "before-after": {
        "prompt": (
            "Split screen comparison. Left side: a confusing government form in "
            "dense Spanish legal text, desaturated cold tones, slight blur. "
            "Right side: a clean WhatsApp conversation with simple clear "
            "instructions, warm golden tones, sharp focus. The contrast between "
            f"bureaucracy (cold grey) and Clara (warm {CLARA_ORANGE}) is dramatic. "
            "Cinematic photography style."
        ),
        "output": "design/mockups/before-after-split.png",
    },
    # --- City/environment scenes ---
    "spanish-city": {
        "prompt": (
            "Wide aerial shot slowly descending over a diverse Spanish neighborhood, "
            "showing a mix of old and modern buildings, small shops with multilingual "
            "signs, people walking on sunny streets. Mediterranean sunlight. "
            f"Warm color grading with blue ({CLARA_BLUE}) sky tones. Cinematic "
            "drone footage style. Hopeful, vibrant mood. Photorealistic 8K."
        ),
        "output": "design/mockups/spanish-city-aerial.png",
    },
    "closing-walk": {
        "prompt": (
            "Wide shot of a diverse group of people walking together on a sunlit "
            "Spanish street, seen from behind. They walk toward a bright horizon. "
            "Golden hour lighting creates long shadows. Cinematic style. Warm "
            "color palette with blue sky. Hopeful, forward-looking, united. "
            + CLARA_STYLE_SUFFIX
        ),
        "output": "design/mockups/closing-walk.png",
    },
    # --- Abstract/background ---
    "gradient-bg": {
        "prompt": (
            "Smooth abstract background with flowing gradients transitioning between "
            f"deep blue ({CLARA_BLUE}), warm orange ({CLARA_ORANGE}), and forest "
            f"green ({CLARA_GREEN}). Subtle particle effects floating upward like "
            "fireflies. Clean, modern, calming. Perfect for text overlay. Minimal "
            "style. 4K resolution."
        ),
        "output": "design/mockups/gradient-background.png",
    },
    # --- Como-usar tutorial steps ---
    "step-1-open": {
        "prompt": (
            "Close-up of hands holding a smartphone opening WhatsApp. "
            "Warm golden morning light from a window. Mediterranean kitchen "
            "background slightly blurred. The hands belong to a middle-aged woman."
        ),
        "output": "clara-web/public/media/steps/step-1-open.png",
    },
    "step-2-language": {
        "prompt": (
            "Over-the-shoulder shot of a person looking at phone screen "
            "showing language options as colorful pill buttons. Soft warm lighting. "
            "Modern minimalist interface visible on screen."
        ),
        "output": "clara-web/public/media/steps/step-2-language.png",
    },
    "step-3-speak": {
        "prompt": (
            "Medium close-up of a young man of Senegalese descent holding "
            "phone to his mouth recording a voice message. Park bench in "
            "a Spanish city. Warm afternoon sunlight through trees."
        ),
        "output": "clara-web/public/media/steps/step-3-speak.png",
    },
    "step-4-response": {
        "prompt": (
            "Medium shot of a woman reading a message on her phone with a "
            "relieved understanding smile. Bright community center. Warm "
            "natural light. Her expression shows the moment of understanding."
        ),
        "output": "clara-web/public/media/steps/step-4-response.png",
    },
}


def load_api_key() -> str:
    """Load GEMINI_API_KEY from env or .env file."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if api_key:
        return api_key

    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("GEMINI_API_KEY="):
                    return line.split("=", 1)[1].strip().strip("'\"")

    print("Error: GEMINI_API_KEY not found in environment or .env", file=sys.stderr)
    sys.exit(1)


def generate_with_imagen(client, prompt: str, output_path: str, aspect_ratio: str = "1:1") -> str:
    """Generate image using Imagen 4.0 (dedicated image model)."""
    from google.genai import types

    response = client.models.generate_images(
        model="imagen-4.0-generate-001",
        prompt=prompt,
        config=types.GenerateImagesConfig(
            number_of_images=1,
            aspect_ratio=aspect_ratio,
        ),
    )
    if response.generated_images:
        img = response.generated_images[0]
        img.image.save(output_path)
        return output_path
    raise RuntimeError("Imagen 4.0 returned no images")


def generate_with_flash(client, prompt: str, output_path: str) -> str:
    """Generate image using Gemini 2.5 Flash Image (free tier friendly)."""
    from google.genai import types

    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            with open(output_path, "wb") as f:
                f.write(part.inline_data.data)
            return output_path

    raise RuntimeError("Gemini Flash returned no image data")


def generate_image(
    prompt: str,
    output_path: str = "generated.png",
    model: str = "auto",
    aspect_ratio: str = "1:1",
    retry_count: int = 2,
) -> str:
    """Generate an image with automatic fallback.

    Model priority:
      "auto"   -> Imagen 4.0 first, fallback to Gemini Flash
      "imagen" -> Imagen 4.0 only
      "flash"  -> Gemini 2.5 Flash Image only
    """
    from google import genai

    api_key = load_api_key()
    client = genai.Client(api_key=api_key)

    # Ensure output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    for attempt in range(retry_count + 1):
        try:
            if model in ("auto", "imagen"):
                try:
                    result = generate_with_imagen(client, prompt, output_path, aspect_ratio)
                    print(f"[Imagen 4.0] Image saved to {result}")
                    return result
                except Exception as e:
                    if model == "imagen":
                        raise
                    print(f"[Imagen 4.0] Failed: {e}", file=sys.stderr)
                    print("[Imagen 4.0] Falling back to Gemini Flash...", file=sys.stderr)

            if model in ("auto", "flash"):
                result = generate_with_flash(client, prompt, output_path)
                print(f"[Gemini Flash] Image saved to {result}")
                return result

        except Exception as e:
            if attempt < retry_count:
                wait = 2 ** attempt * 5
                print(f"Attempt {attempt + 1} failed: {e}. Retrying in {wait}s...", file=sys.stderr)
                time.sleep(wait)
            else:
                raise

    raise RuntimeError("All generation attempts failed")


def list_presets():
    """Print all available presets."""
    print("\nAvailable presets:\n")
    for name, cfg in PRESETS.items():
        prompt_preview = cfg["prompt"][:80] + "..."
        print(f"  {name:20s} -> {cfg['output']}")
        print(f"  {'':20s}    {prompt_preview}\n")


def main():
    parser = argparse.ArgumentParser(
        description="Generate photorealistic images for Clara project",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    parser.add_argument("prompt", nargs="?", help="Text prompt for image generation")
    parser.add_argument("output", nargs="?", default=None, help="Output file path (default: generated.png)")
    parser.add_argument("--model", choices=["auto", "imagen", "flash"], default="auto",
                        help="Model to use (default: auto with fallback)")
    parser.add_argument("--aspect", default="1:1", help="Aspect ratio: 1:1, 16:9, 9:16, 4:3, 3:4")
    parser.add_argument("--preset", help="Use a predefined prompt preset")
    parser.add_argument("--list-presets", action="store_true", help="List all available presets")
    parser.add_argument("--batch", nargs="+", help="Generate multiple presets: --batch maria ahmed fatima")

    args = parser.parse_args()

    if args.list_presets:
        list_presets()
        return

    # Batch mode
    if args.batch:
        project_root = Path(__file__).resolve().parent.parent.parent
        results = []
        for preset_name in args.batch:
            if preset_name not in PRESETS:
                print(f"Unknown preset: {preset_name}. Skipping.", file=sys.stderr)
                continue
            cfg = PRESETS[preset_name]
            output = str(project_root / cfg["output"])
            print(f"\n--- Generating preset '{preset_name}' ---")
            try:
                result = generate_image(cfg["prompt"], output, model=args.model, aspect_ratio=args.aspect)
                results.append((preset_name, result))
            except Exception as e:
                print(f"Failed to generate {preset_name}: {e}", file=sys.stderr)
                results.append((preset_name, None))
            # Rate limiting pause between batch generations
            time.sleep(3)

        print("\n--- Batch Results ---")
        for name, path in results:
            status = path if path else "FAILED"
            print(f"  {name}: {status}")
        return

    # Single preset mode
    if args.preset:
        if args.preset not in PRESETS:
            print(f"Unknown preset: {args.preset}. Use --list-presets to see options.", file=sys.stderr)
            sys.exit(1)
        cfg = PRESETS[args.preset]
        prompt = cfg["prompt"]
        project_root = Path(__file__).resolve().parent.parent.parent
        output = args.output or str(project_root / cfg["output"])
    elif args.prompt:
        prompt = args.prompt
        output = args.output or "generated.png"
    else:
        parser.print_help()
        sys.exit(1)

    generate_image(prompt, output, model=args.model, aspect_ratio=args.aspect)


if __name__ == "__main__":
    main()
