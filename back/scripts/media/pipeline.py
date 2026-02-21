#!/usr/bin/env python3
"""Master media production pipeline for Clara hackathon videos.

Orchestrates the full end-to-end workflow:
  1. Generate photorealistic images (Imagen/Gemini)
  2. Upscale images to 4K (Real-ESRGAN/Replicate/Pillow)
  3. Animate images into video clips (Veo/FAL/Replicate/Ken Burns)
  4. Generate voiceover narration (Edge TTS/ElevenLabs/Gemini/gTTS)
  5. Compose final video (FFmpeg)

Usage:
    # Full pipeline: generate everything from scratch
    python scripts/media/pipeline.py --full -o design/videos/demo/

    # Quick demo: use existing mockup images, add Ken Burns + voiceover
    python scripts/media/pipeline.py --quick -o design/videos/demo/

    # Just images: generate all persona images
    python scripts/media/pipeline.py --images-only -o design/mockups/

    # Just video: compose from existing clips
    python scripts/media/pipeline.py --compose-only -o design/videos/demo/final.mp4

    # Specific video preset
    python scripts/media/pipeline.py --preset elevator-30s -o design/videos/promo/elevator.mp4
    python scripts/media/pipeline.py --preset demo-90s -o design/videos/demo/demo.mp4
"""

import argparse
import glob
import os
import sys
import time
from pathlib import Path

# Add scripts/media to path for imports
sys.path.insert(0, str(Path(__file__).resolve().parent))

PROJECT_ROOT = Path(__file__).resolve().parent.parent.parent


def step_banner(step_num: int, title: str):
    """Print a visible step banner."""
    print(f"\n{'='*60}")
    print(f"  STEP {step_num}: {title}")
    print(f"{'='*60}\n")


def run_full_pipeline(output_dir: str, skip_upscale: bool = False):
    """Run the complete media production pipeline."""
    from generate_image import generate_image, PRESETS as IMG_PRESETS
    from upscale_image import upscale_image
    from image_to_video import image_to_video
    from generate_voiceover import generate_voiceover, NARRATION_SCRIPTS
    from compose_video import concatenate_clips, add_audio, create_title_card, create_image_slideshow

    os.makedirs(output_dir, exist_ok=True)
    images_dir = os.path.join(output_dir, "images")
    clips_dir = os.path.join(output_dir, "clips")
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(images_dir, exist_ok=True)
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # ===== STEP 1: Generate Images =====
    step_banner(1, "GENERATE PHOTOREALISTIC IMAGES")

    persona_presets = ["maria", "ahmed", "fatima", "hands-phone", "spanish-city", "closing-walk"]
    generated_images = []

    for preset_name in persona_presets:
        if preset_name not in IMG_PRESETS:
            continue
        output_path = os.path.join(images_dir, f"{preset_name}.png")
        if os.path.exists(output_path):
            print(f"  [Skip] {preset_name} already exists")
            generated_images.append(output_path)
            continue

        try:
            cfg = IMG_PRESETS[preset_name]
            result = generate_image(cfg["prompt"], output_path, model="auto", aspect_ratio="16:9")
            generated_images.append(result)
            time.sleep(3)  # Rate limiting
        except Exception as e:
            print(f"  [Error] Failed to generate {preset_name}: {e}")

    print(f"\n  Generated {len(generated_images)} images")

    # ===== STEP 2: Upscale Images =====
    if not skip_upscale:
        step_banner(2, "UPSCALE IMAGES TO 4K")
        upscaled_images = []
        for img_path in generated_images:
            basename = Path(img_path).stem
            upscaled_path = os.path.join(images_dir, f"{basename}_4k.png")
            if os.path.exists(upscaled_path):
                print(f"  [Skip] {basename}_4k already exists")
                upscaled_images.append(upscaled_path)
                continue
            try:
                result = upscale_image(img_path, upscaled_path, method="auto", target_width=3840)
                upscaled_images.append(result)
            except Exception as e:
                print(f"  [Error] Failed to upscale {basename}: {e}")
                upscaled_images.append(img_path)  # Use original as fallback

        print(f"\n  Upscaled {len(upscaled_images)} images")
        final_images = upscaled_images
    else:
        final_images = generated_images

    # ===== STEP 3: Animate Images into Video Clips =====
    step_banner(3, "ANIMATE IMAGES INTO VIDEO CLIPS")

    motion_prompts = {
        "maria": "Camera slowly dollies forward toward the woman's face. She looks up from her phone with a warm, relieved expression. Warm golden light.",
        "ahmed": "Subtle camera push in. The man records a voice message, slight breeze moves the leaves behind him. Natural movement.",
        "fatima": "Gentle camera movement. The mother and children look at the phone together, natural subtle gestures.",
        "hands-phone": "Close-up. Thumb presses a button on the phone screen. Subtle hand movement. Warm lighting.",
        "spanish-city": "Slow aerial descent over the neighborhood. People walking. Sunlight moves across buildings.",
        "closing-walk": "Slow motion. The group walks forward together. Golden light creates long shadows. Hopeful mood.",
    }

    video_clips = []
    for img_path in final_images:
        basename = Path(img_path).stem.replace("_4k", "")
        clip_path = os.path.join(clips_dir, f"{basename}.mp4")
        if os.path.exists(clip_path):
            print(f"  [Skip] {basename}.mp4 already exists")
            video_clips.append(clip_path)
            continue

        prompt = motion_prompts.get(basename, "Subtle natural movement, documentary cinematic style")
        try:
            result = image_to_video(img_path, clip_path, prompt, method="auto", duration=6)
            video_clips.append(result)
            time.sleep(2)
        except Exception as e:
            print(f"  [Error] Failed to animate {basename}: {e}")

    print(f"\n  Created {len(video_clips)} video clips")

    # ===== STEP 4: Generate Voiceover =====
    step_banner(4, "GENERATE VOICEOVER NARRATION")

    narrations = {}
    for preset_name, cfg in NARRATION_SCRIPTS.items():
        audio_path = os.path.join(audio_dir, f"narration_{preset_name}.mp3")
        if os.path.exists(audio_path):
            print(f"  [Skip] narration_{preset_name} already exists")
            narrations[preset_name] = audio_path
            continue
        try:
            result = generate_voiceover(cfg["text"], audio_path, method="auto", lang=cfg["lang"])
            narrations[preset_name] = result
            time.sleep(1)
        except Exception as e:
            print(f"  [Error] Failed to generate narration {preset_name}: {e}")

    print(f"\n  Generated {len(narrations)} narration tracks")

    # ===== STEP 5: Compose Final Videos =====
    step_banner(5, "COMPOSE FINAL VIDEOS")

    # 5a: 30-second elevator pitch
    if video_clips and "elevator-30s" in narrations:
        elevator_path = os.path.join(output_dir, "elevator-30s.mp4")
        print("\n  Building 30s elevator pitch...")

        import tempfile
        title_clip = os.path.join(tempfile.gettempdir(), "elevator_title.mp4")
        closing_clip = os.path.join(tempfile.gettempdir(), "elevator_closing.mp4")

        create_title_card("4.5 millones", title_clip,
                          subtitle="de personas no acceden a ayudas que les corresponden",
                          duration=4)
        create_title_card("Tu voz tiene poder", closing_clip,
                          subtitle="Clara | OdiseIA4Good 2026",
                          duration=4)

        # Use first 3 clips + title + closing
        all_clips = [title_clip] + video_clips[:3] + [closing_clip]
        temp_video = os.path.join(tempfile.gettempdir(), "elevator_noaudio.mp4")
        concatenate_clips(all_clips, temp_video, "crossfade", 0.5)
        add_audio(temp_video, narrations["elevator-30s"], elevator_path, replace=True)
        print(f"  -> {elevator_path}")

    # 5b: 90-second demo
    if video_clips and "demo-90s" in narrations:
        demo_path = os.path.join(output_dir, "demo-90s.mp4")
        print("\n  Building 90s demo video...")

        import tempfile
        title1 = os.path.join(tempfile.gettempdir(), "demo_title1.mp4")
        title2 = os.path.join(tempfile.gettempdir(), "demo_title2.mp4")
        title3 = os.path.join(tempfile.gettempdir(), "demo_title3.mp4")
        closing = os.path.join(tempfile.gettempdir(), "demo_closing.mp4")

        create_title_card("Clara", title1, subtitle="Tu asistente de derechos en WhatsApp", duration=3)
        create_title_card("10 millones de inmigrantes", title2, subtitle="67% enfrentan barreras burocraticas", duration=4)
        create_title_card("Open source. Gratis. Siempre.", title3, subtitle="532 tests. Desplegada y funcionando.", duration=4)
        create_title_card("Tu voz tiene poder", closing, subtitle="Clara | OdiseIA4Good 2026 | UDIT Madrid", duration=5)

        all_clips = [title1, title2] + video_clips + [title3, closing]
        temp_video = os.path.join(tempfile.gettempdir(), "demo_noaudio.mp4")
        concatenate_clips(all_clips, temp_video, "crossfade", 0.5)
        add_audio(temp_video, narrations["demo-90s"], demo_path, replace=True)
        print(f"  -> {demo_path}")

    # Summary
    step_banner(6, "PIPELINE COMPLETE")
    print("  Generated assets:")
    print(f"    Images:     {images_dir}/")
    print(f"    Clips:      {clips_dir}/")
    print(f"    Audio:      {audio_dir}/")
    print(f"    Videos:     {output_dir}/")
    print()
    for f in sorted(Path(output_dir).glob("*.mp4")):
        print(f"    -> {f}")


# --- Video presets (image sequence + voiceover -> final video) ---
VIDEO_PRESETS = {
    "como-usar-30s": {
        "images": ["step-1-open", "step-2-language", "step-3-speak", "step-4-response"],
        "voiceover": "como-usar-30s",
        "output": "clara-web/public/media/video/como-usar-clara.mp4",
    },
}


def run_preset_pipeline(preset_name: str, output_override: str = None):
    """Run a preset-based pipeline: generate images + voiceover + compose video."""
    from generate_image import generate_image, PRESETS as IMG_PRESETS
    from image_to_video import animate_kenburns
    from generate_voiceover import generate_voiceover, NARRATION_SCRIPTS
    from compose_video import concatenate_clips, add_audio

    if preset_name not in VIDEO_PRESETS:
        # Fall back to quick pipeline for legacy presets (elevator-30s, demo-90s)
        run_quick_pipeline(output_override)
        return

    cfg = VIDEO_PRESETS[preset_name]
    final_output = output_override or str(PROJECT_ROOT / cfg["output"])

    # Ensure output directory exists
    Path(final_output).parent.mkdir(parents=True, exist_ok=True)

    import tempfile
    temp_dir = os.path.join(tempfile.gettempdir(), f"clara_preset_{preset_name}")
    os.makedirs(temp_dir, exist_ok=True)

    # Step 1: Generate images
    step_banner(1, "GENERATE TUTORIAL IMAGES")
    image_paths = []
    for img_name in cfg["images"]:
        if img_name not in IMG_PRESETS:
            print(f"  [Warning] Unknown image preset: {img_name}", file=sys.stderr)
            continue
        img_cfg = IMG_PRESETS[img_name]
        output_path = str(PROJECT_ROOT / img_cfg["output"])
        if os.path.exists(output_path):
            print(f"  [Skip] {img_name} already exists")
            image_paths.append(output_path)
            continue
        try:
            result = generate_image(img_cfg["prompt"], output_path, model="auto", aspect_ratio="16:9")
            image_paths.append(result)
            time.sleep(3)
        except Exception as e:
            print(f"  [Error] Failed to generate {img_name}: {e}")

    print(f"\n  Prepared {len(image_paths)} images")

    # Step 2: Create Ken Burns video clips from images
    step_banner(2, "ANIMATE IMAGES (KEN BURNS)")
    directions = ["zoom-in", "pan-right", "zoom-out", "pan-left"]
    video_clips = []
    for i, img_path in enumerate(image_paths):
        basename = Path(img_path).stem
        clip_path = os.path.join(temp_dir, f"{basename}.mp4")
        direction = directions[i % len(directions)]
        try:
            result = animate_kenburns(img_path, clip_path, direction=direction, duration=6, fps=30)
            video_clips.append(result)
        except Exception as e:
            print(f"  [Error] {basename}: {e}")

    print(f"\n  Created {len(video_clips)} clips")

    # Step 3: Generate voiceover
    step_banner(3, "GENERATE VOICEOVER")
    vo_name = cfg["voiceover"]
    vo_cfg = NARRATION_SCRIPTS[vo_name]
    audio_path = os.path.join(temp_dir, f"narration_{vo_name}.mp3")
    try:
        generate_voiceover(vo_cfg["text"], audio_path, method="auto", lang=vo_cfg["lang"])
    except Exception as e:
        print(f"  [Error] Voiceover failed: {e}")
        audio_path = None

    # Step 4: Compose final video
    step_banner(4, "COMPOSE FINAL VIDEO")
    if video_clips:
        temp_video = os.path.join(temp_dir, "composed_noaudio.mp4")
        concatenate_clips(video_clips, temp_video, "crossfade", 0.5)
        if audio_path and os.path.exists(audio_path):
            add_audio(temp_video, audio_path, final_output, replace=True)
        else:
            import shutil
            shutil.copy2(temp_video, final_output)
        print(f"\n  -> {final_output}")
    else:
        print("  [Error] No video clips available to compose", file=sys.stderr)

    step_banner(5, "PRESET PIPELINE COMPLETE")
    print(f"  Output: {final_output}")


def run_quick_pipeline(output_dir: str):
    """Quick pipeline: use existing mockup images, Ken Burns + voiceover.

    This works entirely offline/free using:
    - Existing generated images from design/mockups/
    - Ken Burns effect (FFmpeg, local)
    - Edge TTS (free neural voices)
    """
    from image_to_video import animate_kenburns
    from generate_voiceover import generate_voiceover, NARRATION_SCRIPTS
    from compose_video import concatenate_clips, add_audio, create_title_card

    os.makedirs(output_dir, exist_ok=True)
    clips_dir = os.path.join(output_dir, "clips")
    audio_dir = os.path.join(output_dir, "audio")
    os.makedirs(clips_dir, exist_ok=True)
    os.makedirs(audio_dir, exist_ok=True)

    # Find existing mockup images
    mockups_dir = str(PROJECT_ROOT / "design" / "mockups")
    images = sorted(glob.glob(os.path.join(mockups_dir, "v3-*.png")))

    if not images:
        images = sorted(glob.glob(os.path.join(mockups_dir, "*.png")))

    if not images:
        print("Error: No mockup images found in design/mockups/", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(images)} mockup images")

    # Step 1: Create Ken Burns clips from existing images
    step_banner(1, "CREATE KEN BURNS CLIPS FROM EXISTING IMAGES")

    directions = ["zoom-in", "pan-right", "zoom-out", "pan-left", "zoom-in", "pan-down",
                   "zoom-out", "pan-right", "zoom-in", "pan-left"]
    video_clips = []

    for i, img in enumerate(images[:10]):  # Max 10 clips
        basename = Path(img).stem
        clip_path = os.path.join(clips_dir, f"{basename}.mp4")
        direction = directions[i % len(directions)]

        if os.path.exists(clip_path):
            print(f"  [Skip] {basename}.mp4 already exists")
            video_clips.append(clip_path)
            continue

        try:
            result = animate_kenburns(img, clip_path, direction=direction, duration=5, fps=30)
            video_clips.append(result)
        except Exception as e:
            print(f"  [Error] {basename}: {e}")

    print(f"\n  Created {len(video_clips)} clips")

    # Step 2: Generate voiceover
    step_banner(2, "GENERATE VOICEOVER")

    narrations = {}
    for preset_name in ["elevator-30s", "demo-90s"]:
        audio_path = os.path.join(audio_dir, f"narration_{preset_name}.mp3")
        if os.path.exists(audio_path):
            print(f"  [Skip] {preset_name} already exists")
            narrations[preset_name] = audio_path
            continue
        cfg = NARRATION_SCRIPTS[preset_name]
        try:
            result = generate_voiceover(cfg["text"], audio_path, method="auto", lang=cfg["lang"])
            narrations[preset_name] = result
        except Exception as e:
            print(f"  [Error] {preset_name}: {e}")

    # Step 3: Compose videos
    step_banner(3, "COMPOSE FINAL VIDEOS")

    import tempfile

    # Elevator pitch (30s)
    if video_clips and "elevator-30s" in narrations:
        elevator_path = os.path.join(output_dir, "elevator-30s.mp4")
        title_clip = os.path.join(tempfile.gettempdir(), "q_elevator_title.mp4")
        closing_clip = os.path.join(tempfile.gettempdir(), "q_elevator_closing.mp4")
        create_title_card("4.5 millones", title_clip,
                          subtitle="no acceden a sus derechos", duration=4)
        create_title_card("Tu voz tiene poder", closing_clip,
                          subtitle="Clara | OdiseIA4Good 2026", duration=4)

        all_clips = [title_clip] + video_clips[:3] + [closing_clip]
        temp_video = os.path.join(tempfile.gettempdir(), "q_elevator.mp4")
        concatenate_clips(all_clips, temp_video, "crossfade", 0.5)
        add_audio(temp_video, narrations["elevator-30s"], elevator_path, replace=True)
        print(f"  -> {elevator_path}")

    # Demo (90s)
    if video_clips and "demo-90s" in narrations:
        demo_path = os.path.join(output_dir, "demo-90s.mp4")
        title_clip = os.path.join(tempfile.gettempdir(), "q_demo_title.mp4")
        closing_clip = os.path.join(tempfile.gettempdir(), "q_demo_closing.mp4")
        create_title_card("Clara", title_clip,
                          subtitle="Tu voz tiene poder", duration=4)
        create_title_card("Open Source. Gratis. Siempre.", closing_clip,
                          subtitle="Clara | OdiseIA4Good 2026 | UDIT Madrid", duration=5)

        all_clips = [title_clip] + video_clips + [closing_clip]
        temp_video = os.path.join(tempfile.gettempdir(), "q_demo.mp4")
        concatenate_clips(all_clips, temp_video, "crossfade", 0.5)
        add_audio(temp_video, narrations["demo-90s"], demo_path, replace=True)
        print(f"  -> {demo_path}")

    step_banner(4, "QUICK PIPELINE COMPLETE")
    print(f"  Output directory: {output_dir}/")
    for f in sorted(Path(output_dir).glob("*.mp4")):
        print(f"    -> {f}")


def main():
    parser = argparse.ArgumentParser(
        description="Master media production pipeline for Clara",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--full", action="store_true",
                      help="Full pipeline: generate images + upscale + animate + voice + compose")
    mode.add_argument("--quick", action="store_true",
                      help="Quick pipeline: existing images + Ken Burns + Edge TTS")
    mode.add_argument("--images-only", action="store_true",
                      help="Only generate persona images")
    mode.add_argument("--compose-only", action="store_true",
                      help="Only compose video from existing clips/audio")
    mode.add_argument("--preset", choices=["elevator-30s", "demo-90s", "como-usar-30s"],
                      help="Build a specific video preset")

    parser.add_argument("-o", "--output", required=True, help="Output directory or file")
    parser.add_argument("--skip-upscale", action="store_true",
                        help="Skip the upscaling step in full pipeline")

    args = parser.parse_args()

    if args.full:
        run_full_pipeline(args.output, args.skip_upscale)
    elif args.quick:
        run_quick_pipeline(args.output)
    elif args.images_only:
        from generate_image import generate_image, PRESETS
        os.makedirs(args.output, exist_ok=True)
        for name, cfg in PRESETS.items():
            output_path = os.path.join(args.output, f"{name}.png")
            if os.path.exists(output_path):
                print(f"[Skip] {name} already exists")
                continue
            try:
                generate_image(cfg["prompt"], output_path, model="auto", aspect_ratio="16:9")
                time.sleep(3)
            except Exception as e:
                print(f"[Error] {name}: {e}")
    elif args.compose_only:
        from compose_video import main as compose_main
        sys.argv = ["compose_video.py", "-o", args.output]
        compose_main()
    elif args.preset:
        run_preset_pipeline(args.preset, args.output)


if __name__ == "__main__":
    main()
