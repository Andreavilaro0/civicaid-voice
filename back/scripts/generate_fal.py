"""
Generate images and videos using FAL.ai API.

Models available:
  IMAGE:
    - fal-ai/flux-pro/v1.1                ($0.04/MP)   Best quality FLUX 1.1
    - fal-ai/flux-2-pro                   ($0.03/MP)   Latest FLUX 2 Pro
    - fal-ai/flux/dev                      ($0.025/MP)  Good quality, cheaper
    - fal-ai/flux/schnell                  ($0.003/MP)  Fast drafts
    - fal-ai/flux-realism                  (~$0.03/MP)  Photorealism-tuned FLUX
  VIDEO:
    - fal-ai/kling-video/v2.6/pro/image-to-video   ($0.07/s no audio, $0.14/s with audio)
    - fal-ai/minimax/hailuo-02/pro/image-to-video  ($0.08/s)
    - fal-ai/minimax/hailuo-02/pro/text-to-video   ($0.08/s)
    - fal-ai/luma-dream-machine            (~$0.05/s)
    - fal-ai/wan/v2.1/image-to-video       (~$0.05/s)   Open source, cheap
  UPSCALE:
    - fal-ai/aura-sr                       (~$0.01/run)  4x GAN upscaler
    - fal-ai/creative-upscaler             (~$0.05/run)  AI-enhanced upscale

Speed advantage: FAL.ai runs models up to 4x faster than Replicate on average.

Setup:
    pip install fal-client
    export FAL_KEY=...  # from https://fal.ai/dashboard/keys

Usage:
    python scripts/generate_fal.py image "a photo of..." output.png
    python scripts/generate_fal.py image "a photo of..." output.png --model flux-realism
    python scripts/generate_fal.py video "a cinematic shot of..." output.mp4
    python scripts/generate_fal.py video "slow zoom" output.mp4 --image input.png
    python scripts/generate_fal.py upscale input.png output.png
"""

import argparse
import os
import sys
import time
import urllib.request


def _ensure_key():
    """Ensure FAL_KEY is set."""
    key = os.environ.get("FAL_KEY")
    if not key:
        # Try loading from .env
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("FAL_KEY="):
                        key = line.split("=", 1)[1].strip().strip("'\"")
                        os.environ["FAL_KEY"] = key
                        break
    if not key:
        print(
            "Error: FAL_KEY not found.\n"
            "Get one at https://fal.ai/dashboard/keys\n"
            "Then: export FAL_KEY=...",
            file=sys.stderr,
        )
        sys.exit(1)
    return key


def _download_url(url: str, path: str) -> str:
    """Download a URL to a local file."""
    urllib.request.urlretrieve(url, path)
    return path


def _upload_image(image_path: str) -> str:
    """Upload a local image to FAL CDN and return the URL."""
    import fal_client

    url = fal_client.upload_file(image_path)
    print(f"[fal] Uploaded {image_path} -> {url}")
    return url


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

IMAGE_MODELS = {
    "flux-1.1-pro": "fal-ai/flux-pro/v1.1",
    "flux-pro": "fal-ai/flux-pro/v1.1",  # alias
    "flux-2-pro": "fal-ai/flux-2-pro",
    "flux-dev": "fal-ai/flux/dev",
    "flux-schnell": "fal-ai/flux/schnell",
    "flux-realism": "fal-ai/flux-realism",
}


def generate_image(
    prompt: str,
    output_path: str = "output.png",
    model_key: str = "flux-1.1-pro",
    width: int = 1024,
    height: int = 1024,
    num_images: int = 1,
    guidance_scale: float = 3.5,
    num_inference_steps: int = 28,
    seed: int | None = None,
) -> list[str]:
    """Generate image(s) with a FLUX model on FAL.ai.

    Returns list of saved file paths.
    """
    import fal_client

    _ensure_key()

    model_id = IMAGE_MODELS.get(model_key, model_key)
    print(f"[fal] Generating image with {model_id}...")
    print(f"[fal] Prompt: {prompt[:120]}...")

    arguments = {
        "prompt": prompt,
        "image_size": {"width": width, "height": height},
        "num_images": num_images,
        "output_format": "png",
    }

    # Add model-specific params
    if "schnell" not in model_id:
        arguments["guidance_scale"] = guidance_scale
        arguments["num_inference_steps"] = num_inference_steps
    if seed is not None:
        arguments["seed"] = seed

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(f"  [fal] {log['message']}")

    t0 = time.time()
    result = fal_client.subscribe(
        model_id,
        arguments=arguments,
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    elapsed = time.time() - t0

    # Extract image URLs from result
    images = result.get("images", [])
    if not images:
        print("[fal] No images in response", file=sys.stderr)
        sys.exit(1)

    saved = []
    for i, img_data in enumerate(images):
        url = img_data.get("url", "")
        if not url:
            continue

        if num_images > 1:
            base, ext = os.path.splitext(output_path)
            path = f"{base}_{i}{ext}"
        else:
            path = output_path

        _download_url(url, path)
        saved.append(path)
        print(f"[fal] Saved: {path}")

    print(f"[fal] Done in {elapsed:.1f}s ({len(saved)} image(s))")
    return saved


# ---------------------------------------------------------------------------
# Video generation
# ---------------------------------------------------------------------------

VIDEO_MODELS = {
    # Image-to-video models
    "kling": "fal-ai/kling-video/v2.6/pro/image-to-video",
    "kling-standard": "fal-ai/kling-video/v2.6/standard/image-to-video",
    "hailuo": "fal-ai/minimax/hailuo-02/pro/image-to-video",
    "hailuo-standard": "fal-ai/minimax/hailuo-02/standard/image-to-video",
    "wan": "fal-ai/wan/v2.1/image-to-video",
    # Text-to-video models
    "hailuo-text": "fal-ai/minimax/hailuo-02/pro/text-to-video",
    "luma": "fal-ai/luma-dream-machine",
}

# Models that support text-to-video (no image required)
TEXT_TO_VIDEO_MODELS = {"hailuo-text", "luma"}


def generate_video(
    prompt: str,
    output_path: str = "output.mp4",
    model_key: str = "kling",
    image_path: str | None = None,
    duration: float = 5.0,
    aspect_ratio: str = "16:9",
) -> str:
    """Generate a video from text prompt or image+prompt.

    For image-to-video, provide image_path.
    Returns path to saved video file.
    """
    import fal_client

    _ensure_key()

    # Auto-select text-to-video model if no image
    if not image_path and model_key not in TEXT_TO_VIDEO_MODELS:
        model_key = "hailuo-text"
        print(f"[fal] No image provided, switching to text-to-video: {model_key}")

    model_id = VIDEO_MODELS.get(model_key, model_key)
    print(f"[fal] Generating video with {model_id}...")
    print(f"[fal] Prompt: {prompt[:120]}...")

    arguments = {"prompt": prompt}

    if image_path:
        image_url = _upload_image(image_path)
        arguments["image_url"] = image_url

    # Model-specific params
    if "kling" in model_id:
        arguments["duration"] = duration
        arguments["aspect_ratio"] = aspect_ratio
    elif "hailuo" in model_id or "minimax" in model_id:
        arguments["prompt_optimizer"] = True

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(f"  [fal] {log['message']}")

    t0 = time.time()
    result = fal_client.subscribe(
        model_id,
        arguments=arguments,
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    elapsed = time.time() - t0

    # Extract video URL
    video_url = None
    if "video" in result:
        video_url = result["video"].get("url")
    elif "video_url" in result:
        video_url = result["video_url"]

    if not video_url:
        print(f"[fal] No video URL in response: {result}", file=sys.stderr)
        sys.exit(1)

    _download_url(video_url, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[fal] Saved: {output_path} ({size_mb:.1f} MB)")
    print(f"[fal] Done in {elapsed:.1f}s")
    return output_path


# ---------------------------------------------------------------------------
# Image upscaling
# ---------------------------------------------------------------------------

UPSCALE_MODELS = {
    "aura-sr": "fal-ai/aura-sr",
    "creative": "fal-ai/creative-upscaler",
}


def upscale_image(
    input_path: str,
    output_path: str = "upscaled.png",
    model_key: str = "aura-sr",
    scale: int = 4,
    prompt: str | None = None,
) -> str:
    """Upscale an image using AuraSR or Creative Upscaler.

    AuraSR: Fast 4x GAN upscaler, no prompt needed.
    Creative: AI-enhanced, uses prompt for detail generation.

    Returns path to saved upscaled image.
    """
    import fal_client

    _ensure_key()

    model_id = UPSCALE_MODELS.get(model_key, model_key)
    print(f"[fal] Upscaling with {model_id} ({scale}x)...")
    print(f"[fal] Input: {input_path}")

    image_url = _upload_image(input_path)

    arguments = {"image_url": image_url}

    if model_key == "creative":
        arguments["scale"] = scale
        if prompt:
            arguments["prompt"] = prompt
        # Creative upscaler uses SD for enhancement
    elif model_key == "aura-sr":
        # AuraSR always does 4x
        arguments["overlapping_tiles"] = True  # better seams

    def on_queue_update(update):
        if isinstance(update, fal_client.InProgress):
            for log in update.logs:
                print(f"  [fal] {log['message']}")

    t0 = time.time()
    result = fal_client.subscribe(
        model_id,
        arguments=arguments,
        with_logs=True,
        on_queue_update=on_queue_update,
    )
    elapsed = time.time() - t0

    # Extract output URL
    output_url = None
    if "image" in result:
        output_url = result["image"].get("url")
    elif "output" in result:
        output_url = result["output"].get("url") if isinstance(result["output"], dict) else result["output"]

    if not output_url:
        print(f"[fal] No output URL in response: {result}", file=sys.stderr)
        sys.exit(1)

    _download_url(output_url, output_path)
    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[fal] Saved: {output_path} ({size_mb:.1f} MB)")
    print(f"[fal] Done in {elapsed:.1f}s")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate images/videos using FAL.ai",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate photorealistic image with FLUX Pro
  python scripts/generate_fal.py image \\
    "Documentary photo of an immigrant family at a Spanish government \\
     office, warm natural light, photorealistic, 35mm film grain" \\
    clara_office.png

  # Photorealism-tuned model
  python scripts/generate_fal.py image \\
    "Portrait of a social worker helping an elderly person fill out \\
     paperwork, natural window light, Madrid office" \\
    social_worker.png --model flux-realism

  # Fast draft ($0.003)
  python scripts/generate_fal.py image \\
    "Government office interior" \\
    draft.png --model flux-schnell

  # Image-to-video with Kling (best quality)
  python scripts/generate_fal.py video \\
    "Gentle slow zoom in, warm natural lighting, subtle movement" \\
    animated.mp4 --image clara_office.png --model kling

  # Text-to-video with Hailuo
  python scripts/generate_fal.py video \\
    "A cinematic slow pan across a busy government office in Madrid, \\
     warm afternoon light through windows, documentary style" \\
    office_pan.mp4

  # Upscale to 4K with AuraSR (fast)
  python scripts/generate_fal.py upscale clara_office.png clara_4k.png

  # AI-enhanced upscale with Creative Upscaler
  python scripts/generate_fal.py upscale \\
    clara_office.png clara_enhanced.png \\
    --model creative --prompt "sharp photorealistic office interior"
        """,
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    # --- image ---
    p_img = subparsers.add_parser("image", help="Generate an image from text")
    p_img.add_argument("prompt", help="Text prompt for image generation")
    p_img.add_argument("output", nargs="?", default="output.png", help="Output path")
    p_img.add_argument(
        "--model",
        default="flux-1.1-pro",
        choices=list(IMAGE_MODELS.keys()),
        help="Model to use (default: flux-1.1-pro)",
    )
    p_img.add_argument("--width", type=int, default=1024)
    p_img.add_argument("--height", type=int, default=1024)
    p_img.add_argument("--num-images", type=int, default=1)
    p_img.add_argument("--guidance", type=float, default=3.5)
    p_img.add_argument("--steps", type=int, default=28)
    p_img.add_argument("--seed", type=int, default=None)

    # --- video ---
    p_vid = subparsers.add_parser("video", help="Generate a video")
    p_vid.add_argument("prompt", help="Text prompt for video generation")
    p_vid.add_argument("output", nargs="?", default="output.mp4", help="Output path")
    p_vid.add_argument(
        "--model",
        default="kling",
        choices=list(VIDEO_MODELS.keys()),
        help="Model to use (default: kling)",
    )
    p_vid.add_argument("--image", dest="image_path", help="Input image for img2vid")
    p_vid.add_argument("--duration", type=float, default=5.0, help="Video duration (s)")
    p_vid.add_argument("--aspect-ratio", default="16:9", help="Aspect ratio")

    # --- upscale ---
    p_up = subparsers.add_parser("upscale", help="Upscale an image")
    p_up.add_argument("input", help="Input image path")
    p_up.add_argument("output", nargs="?", default="upscaled.png", help="Output path")
    p_up.add_argument(
        "--model",
        default="aura-sr",
        choices=list(UPSCALE_MODELS.keys()),
        help="Upscaler model (default: aura-sr)",
    )
    p_up.add_argument("--scale", type=int, default=4, help="Upscale factor")
    p_up.add_argument("--prompt", help="Prompt for creative upscaler")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            model_key=args.model,
            width=args.width,
            height=args.height,
            num_images=args.num_images,
            guidance_scale=args.guidance,
            num_inference_steps=args.steps,
            seed=args.seed,
        )
    elif args.command == "video":
        generate_video(
            prompt=args.prompt,
            output_path=args.output,
            model_key=args.model,
            image_path=args.image_path,
            duration=args.duration,
            aspect_ratio=args.aspect_ratio,
        )
    elif args.command == "upscale":
        upscale_image(
            input_path=args.input,
            output_path=args.output,
            model_key=args.model,
            scale=args.scale,
            prompt=args.prompt,
        )


if __name__ == "__main__":
    main()
