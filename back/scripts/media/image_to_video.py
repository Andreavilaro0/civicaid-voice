#!/usr/bin/env python3
"""Animate a still image into a short video clip (5-10 seconds).

Supports multiple backends:
  1. Google Veo 3.1 via Gemini API (paid tier, $0.50-0.75/sec)
  2. FAL.ai Kling/Hailuo (free credits for new accounts)
  3. Replicate (free $5 credits for new accounts)
  4. Ken Burns effect via FFmpeg (always free, local)

Usage:
    python scripts/media/image_to_video.py input.png output.mp4 "Camera slowly dollies forward"
    python scripts/media/image_to_video.py input.png output.mp4 "Subtle movement" --method veo
    python scripts/media/image_to_video.py input.png output.mp4 "Person turns head" --method fal
    python scripts/media/image_to_video.py input.png output.mp4 --method kenburns --direction zoom-in
"""

import argparse
import base64
import json
import os
import subprocess
import sys
import time
import urllib.request
from pathlib import Path


def load_env():
    """Load environment variables from .env file."""
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if "=" in line and not line.startswith("#"):
                    key, val = line.split("=", 1)
                    if key not in os.environ:
                        os.environ[key] = val.strip().strip("'\"")


def animate_veo(image_path: str, output_path: str, prompt: str, duration: int = 8) -> str:
    """Animate using Google Veo 3.1 via Gemini API.

    Requirements:
      - GEMINI_API_KEY set (paid tier)
      - google-genai>=1.0 installed
    Cost: ~$0.50/second (video only), ~$0.75/second (with audio)
    """
    from google import genai

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise ValueError("GEMINI_API_KEY not set")

    client = genai.Client(api_key=api_key)

    # Read image
    with open(image_path, "rb") as f:
        image_bytes = f.read()

    # Determine MIME type
    ext = Path(image_path).suffix.lower()
    mime_map = {".png": "image/png", ".jpg": "image/jpeg", ".jpeg": "image/jpeg", ".webp": "image/webp"}
    mime_type = mime_map.get(ext, "image/png")

    print(f"[Veo 3.1] Submitting image-to-video request...")
    print(f"[Veo 3.1] Prompt: {prompt}")
    print(f"[Veo 3.1] Estimated cost: ${0.50 * duration:.2f}")

    # Create image part
    from google.genai import types
    image_part = types.Part(inline_data=types.Blob(mime_type=mime_type, data=image_bytes))

    operation = client.models.generate_videos(
        model="veo-3.1-generate-preview",
        prompt=prompt,
        image=image_part,
    )

    # Poll until complete
    print("[Veo 3.1] Waiting for video generation (typically 1-3 minutes)...")
    while not operation.done:
        time.sleep(10)
        operation = client.operations.get(operation)
        print("[Veo 3.1] Still processing...")

    if operation.result and operation.result.generated_videos:
        video = operation.result.generated_videos[0]
        # Download the video
        video_data = client.files.download(file=video.video)
        with open(output_path, "wb") as f:
            f.write(video_data)
        print(f"[Veo 3.1] Video saved to {output_path}")
        return output_path

    raise RuntimeError("Veo 3.1 did not return a video")


def animate_fal(image_path: str, output_path: str, prompt: str, model: str = "kling") -> str:
    """Animate using FAL.ai (Kling or Hailuo models).

    Requirements:
      - FAL_KEY set
      - fal-client installed: pip install fal-client
    Free credits for new accounts. No credit card required to start.
    """
    try:
        import fal_client
    except ImportError:
        print("Installing fal-client...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "fal-client"])
        import fal_client

    fal_key = os.environ.get("FAL_KEY")
    if not fal_key:
        raise ValueError("FAL_KEY not set. Get one free at https://fal.ai/dashboard/keys")

    # Upload image to get a URL
    print(f"[FAL.ai] Uploading image...")
    image_url = fal_client.upload_file(image_path)

    # Select model endpoint
    model_endpoints = {
        "kling": "fal-ai/kling-video/v2.1/standard/image-to-video",
        "kling-pro": "fal-ai/kling-video/v2.1/pro/image-to-video",
        "hailuo": "fal-ai/minimax/hailuo-02/standard/image-to-video",
    }
    endpoint = model_endpoints.get(model, model_endpoints["kling"])

    print(f"[FAL.ai] Generating video with {model} ({endpoint})...")
    print(f"[FAL.ai] Prompt: {prompt}")

    result = fal_client.subscribe(
        endpoint,
        arguments={
            "prompt": prompt,
            "image_url": image_url,
        },
    )

    # Download video
    video_url = result.get("video", {}).get("url") or result.get("video_url")
    if not video_url:
        raise RuntimeError(f"FAL.ai returned no video URL. Response: {json.dumps(result, indent=2)}")

    print(f"[FAL.ai] Downloading video from {video_url}")
    urllib.request.urlretrieve(video_url, output_path)
    print(f"[FAL.ai] Video saved to {output_path}")
    return output_path


def animate_replicate(image_path: str, output_path: str, prompt: str) -> str:
    """Animate using Replicate API. New accounts get $5 free credits."""
    try:
        import replicate
    except ImportError:
        print("Installing replicate...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "replicate"])
        import replicate

    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        raise ValueError("REPLICATE_API_TOKEN not set. Get one at https://replicate.com/account/api-tokens")

    print(f"[Replicate] Uploading and generating video...")
    with open(image_path, "rb") as f:
        output = replicate.run(
            "stability-ai/stable-video-diffusion:3f0457e4619daac51203dedb472816fd4af51f3149fa7a9e0b5ffcf1b8172438",
            input={
                "input_image": f,
                "motion_bucket_id": 127,
                "cond_aug": 0.02,
                "fps": 6,
            },
        )

    # Download
    video_url = str(output)
    urllib.request.urlretrieve(video_url, output_path)
    print(f"[Replicate] Video saved to {output_path}")
    return output_path


def animate_kenburns(
    image_path: str,
    output_path: str,
    direction: str = "zoom-in",
    duration: int = 8,
    fps: int = 30,
) -> str:
    """Create Ken Burns (pan/zoom) effect using FFmpeg. Always free, always works.

    Directions: zoom-in, zoom-out, pan-left, pan-right, pan-up, pan-down
    """
    import shutil
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise FileNotFoundError("ffmpeg not found. Install with: brew install ffmpeg")

    # Get image dimensions
    from PIL import Image
    img = Image.open(image_path)
    w, h = img.size

    # Ensure dimensions are even (required by most codecs)
    w = w if w % 2 == 0 else w - 1
    h = h if h % 2 == 0 else h - 1

    # Output at 1080p for good quality
    out_w, out_h = 1920, 1080

    # Build filter based on direction
    total_frames = duration * fps

    filters = {
        "zoom-in": (
            f"scale={w*2}:{h*2},zoompan=z='min(zoom+0.001,1.5)':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={out_w}x{out_h}:fps={fps}"
        ),
        "zoom-out": (
            f"scale={w*2}:{h*2},zoompan=z='if(eq(on,1),1.5,max(zoom-0.001,1.0))':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)':s={out_w}x{out_h}:fps={fps}"
        ),
        "pan-left": (
            f"scale={w*2}:{h*2},zoompan=z='1.2':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)+on*2':y='ih/2-(ih/zoom/2)':s={out_w}x{out_h}:fps={fps}"
        ),
        "pan-right": (
            f"scale={w*2}:{h*2},zoompan=z='1.2':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)-on*2':y='ih/2-(ih/zoom/2)':s={out_w}x{out_h}:fps={fps}"
        ),
        "pan-up": (
            f"scale={w*2}:{h*2},zoompan=z='1.2':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)+on*1.5':s={out_w}x{out_h}:fps={fps}"
        ),
        "pan-down": (
            f"scale={w*2}:{h*2},zoompan=z='1.2':d={total_frames}"
            f":x='iw/2-(iw/zoom/2)':y='ih/2-(ih/zoom/2)-on*1.5':s={out_w}x{out_h}:fps={fps}"
        ),
    }

    filter_str = filters.get(direction, filters["zoom-in"])

    cmd = [
        ffmpeg,
        "-y",
        "-loop", "1",
        "-i", image_path,
        "-vf", filter_str,
        "-t", str(duration),
        "-pix_fmt", "yuv420p",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        output_path,
    ]

    print(f"[Ken Burns] Creating {direction} effect ({duration}s at {fps}fps)...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg failed: {result.stderr[-500:]}")

    print(f"[Ken Burns] Video saved to {output_path}")
    return output_path


def image_to_video(
    image_path: str,
    output_path: str,
    prompt: str = "Subtle natural movement, cinematic",
    method: str = "auto",
    direction: str = "zoom-in",
    duration: int = 8,
) -> str:
    """Convert a still image to a short video clip.

    Method priority for 'auto':
      1. FAL.ai (if FAL_KEY set) - best quality, free credits
      2. Veo 3.1 (if GEMINI_API_KEY set, paid tier) - high quality
      3. Replicate (if REPLICATE_API_TOKEN set) - free $5 credits
      4. Ken Burns FFmpeg (always available) - basic but reliable
    """
    load_env()
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if method == "veo":
        return animate_veo(image_path, output_path, prompt, duration)
    elif method == "fal":
        return animate_fal(image_path, output_path, prompt)
    elif method == "replicate":
        return animate_replicate(image_path, output_path, prompt)
    elif method == "kenburns":
        return animate_kenburns(image_path, output_path, direction, duration)
    elif method == "auto":
        # Try methods in order of quality/cost
        if os.environ.get("FAL_KEY"):
            try:
                return animate_fal(image_path, output_path, prompt)
            except Exception as e:
                print(f"[Auto] FAL.ai failed: {e}", file=sys.stderr)

        if os.environ.get("GEMINI_API_KEY"):
            try:
                return animate_veo(image_path, output_path, prompt, duration)
            except Exception as e:
                print(f"[Auto] Veo failed: {e}", file=sys.stderr)

        if os.environ.get("REPLICATE_API_TOKEN"):
            try:
                return animate_replicate(image_path, output_path, prompt)
            except Exception as e:
                print(f"[Auto] Replicate failed: {e}", file=sys.stderr)

        print("[Auto] Falling back to Ken Burns effect...", file=sys.stderr)
        return animate_kenburns(image_path, output_path, direction, duration)

    raise ValueError(f"Unknown method: {method}")


def main():
    parser = argparse.ArgumentParser(description="Animate a still image into a video clip")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output video path (.mp4)")
    parser.add_argument("prompt", nargs="?", default="Subtle natural movement, documentary cinematic style",
                        help="Motion/animation prompt")
    parser.add_argument("--method", choices=["auto", "veo", "fal", "replicate", "kenburns"],
                        default="auto", help="Animation method (default: auto)")
    parser.add_argument("--direction", choices=["zoom-in", "zoom-out", "pan-left", "pan-right", "pan-up", "pan-down"],
                        default="zoom-in", help="Ken Burns direction (default: zoom-in)")
    parser.add_argument("--duration", type=int, default=8, help="Duration in seconds (default: 8)")
    parser.add_argument("--fal-model", choices=["kling", "kling-pro", "hailuo"],
                        default="kling", help="FAL.ai model (default: kling)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    image_to_video(args.input, args.output, args.prompt, args.method, args.direction, args.duration)


if __name__ == "__main__":
    main()
