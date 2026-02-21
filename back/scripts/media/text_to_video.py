#!/usr/bin/env python3
"""Generate video directly from a text prompt (text-to-video).

This is a convenience wrapper that either:
  1. Calls the Gemini Veo 3.1 API directly (paid)
  2. Uses FAL.ai text-to-video models (free credits)
  3. Generates an image first, then animates it (2-step pipeline)

Usage:
    python scripts/media/text_to_video.py "A woman smiles while looking at her phone" output.mp4
    python scripts/media/text_to_video.py "Aerial view of Spanish city" output.mp4 --method veo
    python scripts/media/text_to_video.py "Person recording voice message" output.mp4 --method two-step
"""

import argparse
import os
import subprocess
import sys
import tempfile
import time
from pathlib import Path


def load_env():
    """Load .env file."""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = val.strip().strip("'\"")


def text_to_video_veo(prompt: str, output_path: str, duration: int = 8) -> str:
    """Generate video using Google Veo 3.1 (text-to-video).

    Cost: $0.50-0.75/second. High quality.
    """
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    print(f"[Veo 3.1] Text-to-video generation...")
    print(f"[Veo 3.1] Prompt: {prompt}")
    print(f"[Veo 3.1] Estimated cost: ${0.50 * duration:.2f}")

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
    )

    print("[Veo 3.1] Waiting for generation (1-3 minutes)...")
    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)
        print("[Veo 3.1] Still processing...")

    if operation.result and operation.result.generated_videos:
        video = operation.result.generated_videos[0]
        video_data = client.files.download(file=video.video)
        with open(output_path, "wb") as f:
            f.write(video_data)
        print(f"[Veo 3.1] Video saved to {output_path}")
        return output_path

    raise RuntimeError("Veo 3.1 returned no video")


def text_to_video_fal(prompt: str, output_path: str, model: str = "kling") -> str:
    """Generate video using FAL.ai text-to-video.

    Free credits for new accounts.
    """
    try:
        import fal_client
    except ImportError:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fal-client"])
        import fal_client

    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        raise ValueError("FAL_KEY not set")

    model_endpoints = {
        "kling": "fal-ai/kling-video/v2.1/standard/text-to-video",
        "hailuo": "fal-ai/minimax/hailuo-02/standard/text-to-video",
    }
    endpoint = model_endpoints.get(model, model_endpoints["kling"])

    print(f"[FAL.ai] Text-to-video with {model}...")
    result = fal_client.subscribe(endpoint, arguments={"prompt": prompt})

    import urllib.request
    video_url = result.get("video", {}).get("url") or result.get("video_url")
    if not video_url:
        raise RuntimeError(f"FAL.ai returned no video. Response: {result}")

    urllib.request.urlretrieve(video_url, output_path)
    print(f"[FAL.ai] Video saved to {output_path}")
    return output_path


def text_to_video_twostep(prompt: str, output_path: str) -> str:
    """Two-step pipeline: generate image first, then animate.

    This uses the existing generate_image.py and image_to_video.py scripts.
    Works with free tiers since image generation is free.
    """
    scripts_dir = Path(__file__).resolve().parent

    # Step 1: Generate image
    temp_image = os.path.join(tempfile.gettempdir(), "t2v_image.png")
    print(f"[Two-Step] Step 1: Generating base image...")

    # Import the generate_image module
    sys.path.insert(0, str(scripts_dir))
    from generate_image import generate_image
    generate_image(prompt, temp_image, model="auto", aspect_ratio="16:9")

    # Step 2: Animate the image
    print(f"[Two-Step] Step 2: Animating image to video...")
    from image_to_video import image_to_video
    image_to_video(temp_image, output_path, prompt, method="auto")

    # Clean up
    try:
        os.unlink(temp_image)
    except OSError:
        pass

    return output_path


def text_to_video(
    prompt: str,
    output_path: str,
    method: str = "auto",
    duration: int = 8,
) -> str:
    """Generate video from text prompt.

    Method priority for 'auto':
      1. FAL.ai (if FAL_KEY set) - free credits
      2. Two-step pipeline (image -> video) - uses free tiers
      3. Veo 3.1 (if GEMINI_API_KEY set, paid)
    """
    load_env()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if method == "veo":
        return text_to_video_veo(prompt, output_path, duration)
    elif method == "fal":
        return text_to_video_fal(prompt, output_path)
    elif method == "two-step":
        return text_to_video_twostep(prompt, output_path)
    elif method == "auto":
        if os.environ.get("FAL_KEY"):
            try:
                return text_to_video_fal(prompt, output_path)
            except Exception as e:
                print(f"[Auto] FAL.ai failed: {e}", file=sys.stderr)

        # Two-step is a reliable fallback using free image generation + kenburns
        try:
            return text_to_video_twostep(prompt, output_path)
        except Exception as e:
            print(f"[Auto] Two-step failed: {e}", file=sys.stderr)

        if os.environ.get("GEMINI_API_KEY"):
            return text_to_video_veo(prompt, output_path, duration)

        raise RuntimeError("No generation method available. Set FAL_KEY or GEMINI_API_KEY.")

    raise ValueError(f"Unknown method: {method}")


def main():
    parser = argparse.ArgumentParser(description="Generate video from text prompt")
    parser.add_argument("prompt", help="Text prompt describing the video")
    parser.add_argument("output", help="Output video path (.mp4)")
    parser.add_argument("--method", choices=["auto", "veo", "fal", "two-step"],
                        default="auto", help="Generation method (default: auto)")
    parser.add_argument("--duration", type=int, default=8, help="Target duration (seconds)")

    args = parser.parse_args()
    text_to_video(args.prompt, args.output, args.method, args.duration)


if __name__ == "__main__":
    main()
