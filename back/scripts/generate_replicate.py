"""
Generate images and videos using Replicate.com API.

Models available:
  IMAGE:
    - black-forest-labs/flux-1.1-pro       ($0.04/image)  Best quality
    - black-forest-labs/flux-dev            ($0.03/image)  Good quality, open weights
    - black-forest-labs/flux-schnell        ($0.003/image) Fast drafts
    - bytedance/sdxl-lightning-4step        (~$0.002/run)  Ultra-fast SDXL
    - black-forest-labs/flux-2-pro          ($0.05/image)  Latest FLUX 2
  VIDEO:
    - minimax/video-01                      (~$0.50/video) 6s video, text or image
    - minimax/video-01-live                 (~$0.50/video) Image-to-video, animation
    - luma/ray-2-flash                      (~$0.30/video) Fast cinematic video
  UPSCALE:
    - nightmareai/real-esrgan               (~$0.024/run)  4x upscale
    - daanelson/real-esrgan-a100            (~$0.004/run)  4x upscale (cheaper)
    - philz1337x/clarity-upscaler           (~$0.14/run)   AI-enhanced upscale

Setup:
    pip install replicate
    export REPLICATE_API_TOKEN=r8_...  # from https://replicate.com/account/api-tokens

Usage:
    python scripts/generate_replicate.py image "a photo of..." output.png
    python scripts/generate_replicate.py image "a photo of..." output.png --model flux-schnell
    python scripts/generate_replicate.py video "a cinematic shot of..." output.mp4
    python scripts/generate_replicate.py video output.mp4 --image input.png --prompt "slow zoom"
    python scripts/generate_replicate.py upscale input.png output.png
    python scripts/generate_replicate.py upscale input.png output.png --scale 4
"""

import argparse
import os
import sys
import time
import urllib.request


def _ensure_token():
    """Ensure REPLICATE_API_TOKEN is set."""
    token = os.environ.get("REPLICATE_API_TOKEN")
    if not token:
        # Try loading from .env
        env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
        if os.path.exists(env_path):
            with open(env_path) as f:
                for line in f:
                    line = line.strip()
                    if line.startswith("REPLICATE_API_TOKEN="):
                        token = line.split("=", 1)[1].strip().strip("'\"")
                        os.environ["REPLICATE_API_TOKEN"] = token
                        break
    if not token:
        print(
            "Error: REPLICATE_API_TOKEN not found.\n"
            "Get one at https://replicate.com/account/api-tokens\n"
            "Then: export REPLICATE_API_TOKEN=r8_...",
            file=sys.stderr,
        )
        sys.exit(1)
    return token


# ---------------------------------------------------------------------------
# Image generation
# ---------------------------------------------------------------------------

IMAGE_MODELS = {
    "flux-1.1-pro": "black-forest-labs/flux-1.1-pro",
    "flux-pro": "black-forest-labs/flux-1.1-pro",  # alias
    "flux-2-pro": "black-forest-labs/flux-2-pro",
    "flux-dev": "black-forest-labs/flux-dev",
    "flux-schnell": "black-forest-labs/flux-schnell",
    "sdxl-lightning": "bytedance/sdxl-lightning-4step",
}


def generate_image(
    prompt: str,
    output_path: str = "output.png",
    model_key: str = "flux-1.1-pro",
    width: int = 1024,
    height: int = 1024,
    num_outputs: int = 1,
    guidance_scale: float = 3.5,
    num_inference_steps: int = 28,
    seed: int | None = None,
) -> list[str]:
    """Generate image(s) with a FLUX or SDXL model on Replicate.

    Returns list of saved file paths.
    """
    import replicate

    _ensure_token()

    model_id = IMAGE_MODELS.get(model_key, model_key)
    print(f"[replicate] Generating image with {model_id}...")
    print(f"[replicate] Prompt: {prompt[:120]}...")

    # Build input params — different models accept different params
    input_params = {"prompt": prompt}

    if "schnell" in model_id:
        # Schnell: fast mode, fewer params
        input_params["num_outputs"] = num_outputs
        input_params["aspect_ratio"] = "1:1" if width == height else "16:9"
        input_params["output_format"] = "png"
    elif "sdxl" in model_id:
        input_params["width"] = width
        input_params["height"] = height
        input_params["num_outputs"] = num_outputs
        input_params["scheduler"] = "K_EULER"
        input_params["num_inference_steps"] = 4
    else:
        # FLUX Pro / Dev
        input_params["width"] = width
        input_params["height"] = height
        input_params["num_outputs"] = num_outputs
        input_params["guidance"] = guidance_scale
        input_params["num_inference_steps"] = num_inference_steps
        input_params["output_format"] = "png"
        if seed is not None:
            input_params["seed"] = seed

    t0 = time.time()
    output = replicate.run(model_id, input=input_params)
    elapsed = time.time() - t0

    # Handle output — can be list of FileOutput or list of URLs
    saved = []
    items = output if isinstance(output, list) else [output]
    for i, item in enumerate(items):
        if num_outputs > 1:
            base, ext = os.path.splitext(output_path)
            path = f"{base}_{i}{ext}"
        else:
            path = output_path

        if hasattr(item, "read"):
            # FileOutput object
            with open(path, "wb") as f:
                f.write(item.read())
        elif isinstance(item, str) and item.startswith("http"):
            # URL string
            urllib.request.urlretrieve(item, path)
        else:
            print(f"[replicate] Unexpected output type: {type(item)}", file=sys.stderr)
            continue

        saved.append(path)
        print(f"[replicate] Saved: {path}")

    print(f"[replicate] Done in {elapsed:.1f}s ({len(saved)} image(s))")
    return saved


# ---------------------------------------------------------------------------
# Video generation
# ---------------------------------------------------------------------------

VIDEO_MODELS = {
    "minimax": "minimax/video-01",
    "minimax-live": "minimax/video-01-live",
    "luma-flash": "luma/ray-2-flash",
}


def generate_video(
    prompt: str,
    output_path: str = "output.mp4",
    model_key: str = "minimax",
    image_path: str | None = None,
    duration: int = 6,
) -> str:
    """Generate a video from text prompt or image+prompt.

    For image-to-video, provide image_path.
    Returns path to saved video file.
    """
    import replicate

    _ensure_token()

    # If image provided, prefer image-to-video models
    if image_path and model_key == "minimax":
        model_key = "minimax-live"

    model_id = VIDEO_MODELS.get(model_key, model_key)
    print(f"[replicate] Generating video with {model_id}...")
    print(f"[replicate] Prompt: {prompt[:120]}...")

    input_params = {"prompt": prompt}

    if image_path:
        print(f"[replicate] Input image: {image_path}")
        input_params["first_frame_image"] = open(image_path, "rb")

    t0 = time.time()
    output = replicate.run(model_id, input=input_params)
    elapsed = time.time() - t0

    # Save video
    if hasattr(output, "read"):
        with open(output_path, "wb") as f:
            f.write(output.read())
    elif isinstance(output, str) and output.startswith("http"):
        urllib.request.urlretrieve(output, output_path)
    elif isinstance(output, list) and len(output) > 0:
        item = output[0]
        if hasattr(item, "read"):
            with open(output_path, "wb") as f:
                f.write(item.read())
        elif isinstance(item, str):
            urllib.request.urlretrieve(item, output_path)
    else:
        print(f"[replicate] Unexpected output: {type(output)}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[replicate] Saved: {output_path} ({size_mb:.1f} MB)")
    print(f"[replicate] Done in {elapsed:.1f}s")
    return output_path


# ---------------------------------------------------------------------------
# Image upscaling
# ---------------------------------------------------------------------------

UPSCALE_MODELS = {
    "real-esrgan": "nightmareai/real-esrgan",
    "real-esrgan-fast": "daanelson/real-esrgan-a100",
    "clarity": "philz1337x/clarity-upscaler",
}


def upscale_image(
    input_path: str,
    output_path: str = "upscaled.png",
    model_key: str = "real-esrgan",
    scale: int = 4,
    face_enhance: bool = False,
) -> str:
    """Upscale an image using Real-ESRGAN or Clarity Upscaler.

    Returns path to saved upscaled image.
    """
    import replicate

    _ensure_token()

    model_id = UPSCALE_MODELS.get(model_key, model_key)
    print(f"[replicate] Upscaling with {model_id} (scale={scale}x)...")
    print(f"[replicate] Input: {input_path}")

    input_params = {
        "image": open(input_path, "rb"),
        "scale": scale,
        "face_enhance": face_enhance,
    }

    t0 = time.time()
    output = replicate.run(model_id, input=input_params)
    elapsed = time.time() - t0

    # Save result
    if hasattr(output, "read"):
        with open(output_path, "wb") as f:
            f.write(output.read())
    elif isinstance(output, str) and output.startswith("http"):
        urllib.request.urlretrieve(output, output_path)
    else:
        print(f"[replicate] Unexpected output: {type(output)}", file=sys.stderr)
        sys.exit(1)

    size_mb = os.path.getsize(output_path) / (1024 * 1024)
    print(f"[replicate] Saved: {output_path} ({size_mb:.1f} MB)")
    print(f"[replicate] Done in {elapsed:.1f}s")
    return output_path


# ---------------------------------------------------------------------------
# CLI
# ---------------------------------------------------------------------------

def main():
    parser = argparse.ArgumentParser(
        description="Generate images/videos using Replicate.com",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Generate photorealistic image with FLUX 1.1 Pro
  python scripts/generate_replicate.py image \\
    "Documentary photo of an immigrant family receiving help at a Spanish \\
     government office, warm natural light, photorealistic" \\
    clara_office.png

  # Fast draft with FLUX Schnell ($0.003)
  python scripts/generate_replicate.py image \\
    "A social worker helping an elderly person" \\
    draft.png --model flux-schnell

  # Generate video from text
  python scripts/generate_replicate.py video \\
    "A slow cinematic pan across a government office in Madrid" \\
    office_pan.mp4

  # Image-to-video: animate a generated image
  python scripts/generate_replicate.py video \\
    "Gentle slow zoom in, warm lighting" \\
    animated.mp4 --image clara_office.png

  # Upscale to 4K
  python scripts/generate_replicate.py upscale \\
    clara_office.png clara_office_4k.png --scale 4
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
    p_img.add_argument("--num-outputs", type=int, default=1)
    p_img.add_argument("--guidance", type=float, default=3.5)
    p_img.add_argument("--steps", type=int, default=28)
    p_img.add_argument("--seed", type=int, default=None)

    # --- video ---
    p_vid = subparsers.add_parser("video", help="Generate a video")
    p_vid.add_argument("prompt", help="Text prompt for video generation")
    p_vid.add_argument("output", nargs="?", default="output.mp4", help="Output path")
    p_vid.add_argument(
        "--model",
        default="minimax",
        choices=list(VIDEO_MODELS.keys()),
        help="Model to use (default: minimax)",
    )
    p_vid.add_argument("--image", dest="image_path", help="Input image for img2vid")

    # --- upscale ---
    p_up = subparsers.add_parser("upscale", help="Upscale an image")
    p_up.add_argument("input", help="Input image path")
    p_up.add_argument("output", nargs="?", default="upscaled.png", help="Output path")
    p_up.add_argument(
        "--model",
        default="real-esrgan",
        choices=list(UPSCALE_MODELS.keys()),
        help="Upscaler model (default: real-esrgan)",
    )
    p_up.add_argument("--scale", type=int, default=4, help="Upscale factor")
    p_up.add_argument("--face-enhance", action="store_true", help="Enhance faces")

    args = parser.parse_args()

    if args.command == "image":
        generate_image(
            prompt=args.prompt,
            output_path=args.output,
            model_key=args.model,
            width=args.width,
            height=args.height,
            num_outputs=args.num_outputs,
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
        )
    elif args.command == "upscale":
        upscale_image(
            input_path=args.input,
            output_path=args.output,
            model_key=args.model,
            scale=args.scale,
            face_enhance=args.face_enhance,
        )


if __name__ == "__main__":
    main()
