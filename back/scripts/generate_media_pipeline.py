"""
Full media pipeline: Generate image -> Upscale to 4K -> Animate to video.

Supports both Replicate and FAL.ai backends. Runs the complete workflow:
  1. Text-to-image (photorealistic FLUX Pro)
  2. Upscale to 4K (Real-ESRGAN or AuraSR)
  3. Image-to-video (Kling, Hailuo, or MiniMax)

Designed for Clara/CivicAid documentary-style content about immigrants in Spain.

Setup:
    pip install replicate fal-client
    export REPLICATE_API_TOKEN=r8_...
    export FAL_KEY=...

Usage:
    # Full pipeline with FAL (recommended for speed)
    python scripts/generate_media_pipeline.py \\
      --prompt "Documentary photo of a young immigrant mother receiving \\
        guidance at a Spanish social services office, warm afternoon light" \\
      --backend fal \\
      --output-dir output/clara_scene_01

    # Full pipeline with Replicate
    python scripts/generate_media_pipeline.py \\
      --prompt "Close-up of hands filling out immigration paperwork" \\
      --backend replicate \\
      --output-dir output/clara_scene_02

    # Image only (no video)
    python scripts/generate_media_pipeline.py \\
      --prompt "A social worker in Madrid" \\
      --backend fal --skip-video \\
      --output-dir output/test

    # Start from existing image (skip generation)
    python scripts/generate_media_pipeline.py \\
      --input-image existing.png \\
      --backend fal \\
      --output-dir output/from_existing
"""

import argparse
import os
import sys
import time


# ---------------------------------------------------------------------------
# Clara-specific prompt templates for documentary photorealism
# ---------------------------------------------------------------------------

CLARA_STYLE_SUFFIX = (
    "Photorealistic, documentary style, natural warm lighting, "
    "Canon EOS R5, 35mm f/1.4 lens, shallow depth of field, "
    "film grain, candid moment, editorial photography, "
    "Spanish government office or community center setting"
)

CLARA_NEGATIVE = (
    "cartoon, anime, illustration, painting, drawing, "
    "artificial, plastic, overexposed, underexposed, "
    "blurry, low quality, watermark, text overlay"
)

CLARA_VIDEO_MOTION = (
    "Gentle slow camera movement, subtle ambient motion, "
    "warm natural lighting shifts, documentary cinematography, "
    "handheld feel, 24fps cinematic"
)


def enhance_prompt(prompt: str, add_style: bool = True) -> str:
    """Add Clara documentary-style suffix to a prompt."""
    if add_style and CLARA_STYLE_SUFFIX not in prompt:
        return f"{prompt}. {CLARA_STYLE_SUFFIX}"
    return prompt


# ---------------------------------------------------------------------------
# Pipeline steps
# ---------------------------------------------------------------------------

def step_generate_image(
    prompt: str,
    output_dir: str,
    backend: str = "fal",
    width: int = 1024,
    height: int = 1024,
) -> str:
    """Step 1: Generate a photorealistic image."""
    output_path = os.path.join(output_dir, "01_generated.png")
    print("\n" + "=" * 60)
    print("STEP 1: Generate Image")
    print("=" * 60)

    if backend == "fal":
        from generate_fal import generate_image
        generate_image(
            prompt=prompt,
            output_path=output_path,
            model_key="flux-realism",
            width=width,
            height=height,
        )
    else:
        from generate_replicate import generate_image
        generate_image(
            prompt=prompt,
            output_path=output_path,
            model_key="flux-1.1-pro",
            width=width,
            height=height,
        )

    return output_path


def step_upscale(
    input_path: str,
    output_dir: str,
    backend: str = "fal",
    scale: int = 4,
) -> str:
    """Step 2: Upscale image to 4K."""
    output_path = os.path.join(output_dir, "02_upscaled.png")
    print("\n" + "=" * 60)
    print("STEP 2: Upscale to 4K")
    print("=" * 60)

    if backend == "fal":
        from generate_fal import upscale_image
        upscale_image(
            input_path=input_path,
            output_path=output_path,
            model_key="aura-sr",
            scale=scale,
        )
    else:
        from generate_replicate import upscale_image
        upscale_image(
            input_path=input_path,
            output_path=output_path,
            model_key="real-esrgan",
            scale=scale,
        )

    return output_path


def step_animate(
    input_path: str,
    prompt: str,
    output_dir: str,
    backend: str = "fal",
) -> str:
    """Step 3: Animate the image into a video."""
    output_path = os.path.join(output_dir, "03_video.mp4")
    print("\n" + "=" * 60)
    print("STEP 3: Animate to Video")
    print("=" * 60)

    video_prompt = f"{prompt}. {CLARA_VIDEO_MOTION}"

    if backend == "fal":
        from generate_fal import generate_video
        generate_video(
            prompt=video_prompt,
            output_path=output_path,
            model_key="kling",
            image_path=input_path,
        )
    else:
        from generate_replicate import generate_video
        generate_video(
            prompt=video_prompt,
            output_path=output_path,
            model_key="minimax-live",
            image_path=input_path,
        )

    return output_path


# ---------------------------------------------------------------------------
# Main pipeline
# ---------------------------------------------------------------------------

def run_pipeline(
    prompt: str,
    output_dir: str,
    backend: str = "fal",
    input_image: str | None = None,
    skip_upscale: bool = False,
    skip_video: bool = False,
    width: int = 1024,
    height: int = 1024,
    enhance: bool = True,
) -> dict:
    """Run the full media generation pipeline.

    Returns dict with paths to all generated files.
    """
    os.makedirs(output_dir, exist_ok=True)

    # Enhance prompt for photorealism
    enhanced_prompt = enhance_prompt(prompt) if enhance else prompt

    # Save prompt to file for reference
    with open(os.path.join(output_dir, "prompt.txt"), "w") as f:
        f.write(f"Original: {prompt}\n")
        f.write(f"Enhanced: {enhanced_prompt}\n")
        f.write(f"Backend: {backend}\n")

    results = {"prompt": enhanced_prompt, "backend": backend}
    t_total = time.time()

    # Step 1: Generate or use existing image
    if input_image:
        image_path = input_image
        print(f"\nUsing existing image: {input_image}")
    else:
        image_path = step_generate_image(
            prompt=enhanced_prompt,
            output_dir=output_dir,
            backend=backend,
            width=width,
            height=height,
        )
    results["image"] = image_path

    # Step 2: Upscale
    if not skip_upscale:
        upscaled_path = step_upscale(
            input_path=image_path,
            output_dir=output_dir,
            backend=backend,
        )
        results["upscaled"] = upscaled_path
        # Use upscaled for video input
        video_input = upscaled_path
    else:
        video_input = image_path

    # Step 3: Animate
    if not skip_video:
        video_path = step_animate(
            input_path=video_input,
            prompt=prompt,  # Use original prompt for motion
            output_dir=output_dir,
            backend=backend,
        )
        results["video"] = video_path

    total_elapsed = time.time() - t_total
    results["total_time"] = total_elapsed

    print("\n" + "=" * 60)
    print("PIPELINE COMPLETE")
    print("=" * 60)
    print(f"Backend: {backend}")
    print(f"Total time: {total_elapsed:.1f}s")
    for key, val in results.items():
        if key not in ("prompt", "backend", "total_time"):
            print(f"  {key}: {val}")

    return results


def main():
    parser = argparse.ArgumentParser(
        description="Full media pipeline: image -> upscale -> video",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Clara Documentary Scene Prompts (ready to use):

  Scene 1 - Office Help:
    "A young immigrant mother sits across from a kind social worker at a
     Spanish government office, warm afternoon light streams through the
     window, paperwork on the desk between them"

  Scene 2 - Community:
    "A diverse group of immigrants at a community center in Madrid, sharing
     a meal together, children playing in the background, warm ambient light"

  Scene 3 - Documentation:
    "Close-up of hands carefully filling out Spanish immigration forms,
     a phone showing a WhatsApp conversation with Clara the AI assistant
     visible nearby"

  Scene 4 - Success:
    "A family celebrating outside a Spanish government building after
     receiving their residency approval, holding documents, genuine joy,
     Barcelona street in background"

  Scene 5 - Clara AI:
    "A smartphone screen showing a WhatsApp conversation with an AI
     assistant named Clara, warm purple chat bubbles, Spanish text,
     a cup of coffee beside the phone on a wooden table"
        """,
    )

    parser.add_argument(
        "--prompt",
        required=False,
        help="Text prompt for image generation",
    )
    parser.add_argument(
        "--input-image",
        help="Skip generation, start from existing image",
    )
    parser.add_argument(
        "--backend",
        choices=["fal", "replicate"],
        default="fal",
        help="Platform to use (default: fal)",
    )
    parser.add_argument(
        "--output-dir",
        default="output/pipeline",
        help="Output directory (default: output/pipeline)",
    )
    parser.add_argument("--width", type=int, default=1024)
    parser.add_argument("--height", type=int, default=1024)
    parser.add_argument("--skip-upscale", action="store_true")
    parser.add_argument("--skip-video", action="store_true")
    parser.add_argument(
        "--no-enhance",
        action="store_true",
        help="Don't add documentary style suffix to prompt",
    )

    args = parser.parse_args()

    if not args.prompt and not args.input_image:
        parser.error("Either --prompt or --input-image is required")

    prompt = args.prompt or "Documentary scene"

    # Add scripts dir to path for imports
    sys.path.insert(0, os.path.dirname(__file__))

    run_pipeline(
        prompt=prompt,
        output_dir=args.output_dir,
        backend=args.backend,
        input_image=args.input_image,
        skip_upscale=args.skip_upscale,
        skip_video=args.skip_video,
        width=args.width,
        height=args.height,
        enhance=not args.no_enhance,
    )


if __name__ == "__main__":
    main()
