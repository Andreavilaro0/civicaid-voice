#!/usr/bin/env python3
"""Upscale images to 4K using Real-ESRGAN (local) or Replicate API.

Methods (in priority order):
  1. Local Real-ESRGAN (free, requires realesrgan-ncnn-vulkan binary)
  2. Replicate API (cloud, $5 free credits for new accounts)
  3. Pillow Lanczos (free, basic but always works)

Usage:
    python scripts/media/upscale_image.py input.png output_4k.png
    python scripts/media/upscale_image.py input.png output_4k.png --method local
    python scripts/media/upscale_image.py input.png output_4k.png --method replicate
    python scripts/media/upscale_image.py input.png output_4k.png --method pillow --scale 4
    python scripts/media/upscale_image.py input.png output_4k.png --target-width 3840
"""

import argparse
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def load_env():
    """Load .env file if REPLICATE_API_TOKEN not already set."""
    if os.environ.get("REPLICATE_API_TOKEN"):
        return
    env_path = Path(__file__).resolve().parent.parent.parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            for line in f:
                line = line.strip()
                if line.startswith("REPLICATE_API_TOKEN="):
                    os.environ["REPLICATE_API_TOKEN"] = line.split("=", 1)[1].strip().strip("'\"")


def upscale_local(input_path: str, output_path: str, scale: int = 4) -> str:
    """Upscale using locally installed Real-ESRGAN binary.

    Install: brew install realesrgan-ncnn-vulkan  (macOS)
    Or download from: https://github.com/xinntao/Real-ESRGAN/releases
    """
    # Check for the binary
    binary = shutil.which("realesrgan-ncnn-vulkan")
    if not binary:
        # Also check common manual install locations
        for path in [
            "/usr/local/bin/realesrgan-ncnn-vulkan",
            os.path.expanduser("~/bin/realesrgan-ncnn-vulkan"),
            os.path.expanduser("~/Real-ESRGAN/realesrgan-ncnn-vulkan"),
        ]:
            if os.path.isfile(path):
                binary = path
                break

    if not binary:
        raise FileNotFoundError(
            "realesrgan-ncnn-vulkan not found. Install it with:\n"
            "  brew install realesrgan-ncnn-vulkan\n"
            "Or download from: https://github.com/xinntao/Real-ESRGAN/releases"
        )

    model_name = "realesrgan-x4plus" if scale == 4 else "realesrgan-x4plus"

    cmd = [
        binary,
        "-i", input_path,
        "-o", output_path,
        "-n", model_name,
        "-s", str(scale),
    ]

    print(f"[Local Real-ESRGAN] Running: {' '.join(cmd)}")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=120)

    if result.returncode != 0:
        raise RuntimeError(f"Real-ESRGAN failed: {result.stderr}")

    print(f"[Local Real-ESRGAN] Upscaled to {output_path}")
    return output_path


def upscale_replicate(input_path: str, output_path: str, scale: int = 4) -> str:
    """Upscale using Replicate API (cloud). New accounts get $5 free credits."""
    load_env()

    try:
        import replicate
    except ImportError:
        print("Installing replicate package...", file=sys.stderr)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "replicate"])
        import replicate

    print(f"[Replicate] Uploading {input_path}...")

    with open(input_path, "rb") as f:
        output = replicate.run(
            "nightmareai/real-esrgan:f121d640bd286e1fdc67f9799164c1d5be36ff74576ee11c803ae5b665dd46aa",
            input={
                "image": f,
                "scale": scale,
                "face_enhance": True,
            },
        )

    # Download the result
    import urllib.request
    print(f"[Replicate] Downloading result...")
    urllib.request.urlretrieve(str(output), output_path)
    print(f"[Replicate] Upscaled to {output_path}")
    return output_path


def upscale_pillow(input_path: str, output_path: str, scale: int = 4, target_width: int = None) -> str:
    """Upscale using Pillow Lanczos resampling (always available, basic quality)."""
    from PIL import Image

    img = Image.open(input_path)
    orig_w, orig_h = img.size

    if target_width:
        new_w = target_width
        new_h = int(orig_h * (target_width / orig_w))
    else:
        new_w = orig_w * scale
        new_h = orig_h * scale

    print(f"[Pillow] Upscaling {orig_w}x{orig_h} -> {new_w}x{new_h}")
    upscaled = img.resize((new_w, new_h), Image.LANCZOS)

    # Optional: apply slight sharpening for better perceived quality
    from PIL import ImageFilter
    upscaled = upscaled.filter(ImageFilter.SHARPEN)

    upscaled.save(output_path, quality=95)
    print(f"[Pillow] Upscaled to {output_path}")
    return output_path


def upscale_image(
    input_path: str,
    output_path: str,
    method: str = "auto",
    scale: int = 4,
    target_width: int = None,
) -> str:
    """Upscale image with automatic method selection.

    Priority: local Real-ESRGAN > Replicate API > Pillow Lanczos
    """
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)

    if method == "local":
        return upscale_local(input_path, output_path, scale)
    elif method == "replicate":
        return upscale_replicate(input_path, output_path, scale)
    elif method == "pillow":
        return upscale_pillow(input_path, output_path, scale, target_width)
    elif method == "auto":
        # Try methods in priority order
        try:
            return upscale_local(input_path, output_path, scale)
        except (FileNotFoundError, RuntimeError) as e:
            print(f"[Auto] Local failed: {e}", file=sys.stderr)

        try:
            return upscale_replicate(input_path, output_path, scale)
        except Exception as e:
            print(f"[Auto] Replicate failed: {e}", file=sys.stderr)

        print("[Auto] Falling back to Pillow Lanczos...", file=sys.stderr)
        return upscale_pillow(input_path, output_path, scale, target_width)

    raise ValueError(f"Unknown method: {method}")


def main():
    parser = argparse.ArgumentParser(description="Upscale images to 4K")
    parser.add_argument("input", help="Input image path")
    parser.add_argument("output", help="Output image path")
    parser.add_argument("--method", choices=["auto", "local", "replicate", "pillow"],
                        default="auto", help="Upscaling method (default: auto)")
    parser.add_argument("--scale", type=int, default=4, help="Scale factor (default: 4)")
    parser.add_argument("--target-width", type=int, default=None,
                        help="Target width in pixels (overrides --scale)")

    args = parser.parse_args()

    if not os.path.isfile(args.input):
        print(f"Error: Input file not found: {args.input}", file=sys.stderr)
        sys.exit(1)

    upscale_image(args.input, args.output, args.method, args.scale, args.target_width)


if __name__ == "__main__":
    main()
