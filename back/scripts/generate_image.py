"""Generate images using Gemini/Imagen API."""

import sys
import os


def generate_image(prompt: str, output_path: str = "generated.png") -> str:
    """Generate an image from a text prompt using Imagen 4.0."""
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    if line.startswith("GEMINI_API_KEY="):
                        api_key = line.strip().split("=", 1)[1].strip().strip("'\"")
                        break

    if not api_key:
        print("Error: GEMINI_API_KEY not found", file=sys.stderr)
        sys.exit(1)

    from google import genai
    from google.genai import types

    client = genai.Client(api_key=api_key)

    # Try Imagen 4.0 first (dedicated image model)
    try:
        response = client.models.generate_images(
            model="imagen-4.0-generate-001",
            prompt=prompt,
            config=types.GenerateImagesConfig(
                number_of_images=1,
            ),
        )
        if response.generated_images:
            img = response.generated_images[0]
            img.image.save(output_path)
            print(f"Image saved to {output_path}")
            return output_path
    except Exception as e:
        print(f"Imagen 4.0 failed: {e}", file=sys.stderr)
        print("Trying Gemini 2.5 Flash Image fallback...", file=sys.stderr)

    # Fallback: Gemini 2.5 Flash with image generation
    response = client.models.generate_content(
        model="gemini-2.5-flash-image",
        contents=prompt,
        config=types.GenerateContentConfig(
            response_modalities=["IMAGE", "TEXT"],
        ),
    )

    for part in response.candidates[0].content.parts:
        if part.inline_data is not None:
            image_data = part.inline_data.data
            with open(output_path, "wb") as f:
                f.write(image_data)
            print(f"Image saved to {output_path}")
            return output_path

    print("No image generated in response", file=sys.stderr)
    sys.exit(1)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python generate_image.py 'prompt' [output_path]")
        sys.exit(1)

    prompt = sys.argv[1]
    output = sys.argv[2] if len(sys.argv) > 2 else "generated.png"
    generate_image(prompt, output)
