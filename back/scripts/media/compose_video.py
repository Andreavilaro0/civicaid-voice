#!/usr/bin/env python3
"""Compose video clips + audio + transitions into final video using FFmpeg.

This is the final step in the media pipeline: combine all generated assets
into polished output videos.

Usage:
    # Concatenate clips with crossfade transitions
    python scripts/media/compose_video.py --clips clip1.mp4 clip2.mp4 clip3.mp4 -o final.mp4

    # Add voiceover to a video
    python scripts/media/compose_video.py --video base.mp4 --audio voiceover.mp3 -o with_narration.mp4

    # Add background music (ducked under voiceover)
    python scripts/media/compose_video.py --video base.mp4 --audio voiceover.mp3 --music bg.mp3 -o final.mp4

    # Full pipeline: clips + voiceover + music + title card
    python scripts/media/compose_video.py \\
        --clips clip1.mp4 clip2.mp4 clip3.mp4 \\
        --audio voiceover.mp3 \\
        --music background.mp3 \\
        --title "Tu voz tiene poder" \\
        --subtitle "Clara | OdiseIA4Good 2026" \\
        -o final.mp4

    # Use a preset composition
    python scripts/media/compose_video.py --preset elevator-30s -o elevator.mp4

    # Add subtitles from SRT file
    python scripts/media/compose_video.py --video base.mp4 --srt subtitles.srt -o subtitled.mp4
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path


def get_ffmpeg():
    """Get ffmpeg path or raise."""
    ffmpeg = shutil.which("ffmpeg")
    if not ffmpeg:
        raise FileNotFoundError("ffmpeg not found. Install with: brew install ffmpeg")
    return ffmpeg


def get_ffprobe():
    """Get ffprobe path or raise."""
    ffprobe = shutil.which("ffprobe")
    if not ffprobe:
        raise FileNotFoundError("ffprobe not found. Install with: brew install ffmpeg")
    return ffprobe


def get_duration(file_path: str) -> float:
    """Get duration of a media file in seconds."""
    ffprobe = get_ffprobe()
    cmd = [
        ffprobe, "-v", "quiet", "-print_format", "json",
        "-show_format", file_path,
    ]
    result = subprocess.run(cmd, capture_output=True, text=True)
    data = json.loads(result.stdout)
    return float(data["format"]["duration"])


def concatenate_clips(
    clips: list,
    output_path: str,
    transition: str = "crossfade",
    transition_duration: float = 0.5,
) -> str:
    """Concatenate video clips with optional transitions.

    Transitions: none, crossfade
    """
    ffmpeg = get_ffmpeg()

    if transition == "none" or len(clips) == 1:
        # Simple concatenation without re-encoding
        with tempfile.NamedTemporaryFile(mode="w", suffix=".txt", delete=False) as f:
            for clip in clips:
                f.write(f"file '{os.path.abspath(clip)}'\n")
            list_file = f.name

        cmd = [
            ffmpeg, "-y", "-f", "concat", "-safe", "0",
            "-i", list_file,
            "-c", "copy",
            output_path,
        ]
        print(f"[Compose] Concatenating {len(clips)} clips (no transition)...")
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
        os.unlink(list_file)

        if result.returncode != 0:
            raise RuntimeError(f"FFmpeg concat failed: {result.stderr[-500:]}")

    elif transition == "crossfade":
        # Build complex filter for crossfades
        if len(clips) == 1:
            shutil.copy(clips[0], output_path)
            return output_path

        # Get durations
        durations = [get_duration(c) for c in clips]
        td = transition_duration

        # Build the filter graph
        inputs = " ".join(f"-i {c}" for c in clips)
        n = len(clips)

        # Start with first clip
        filter_parts = []
        # Normalize all clips to same resolution and fps
        for i in range(n):
            filter_parts.append(f"[{i}:v]scale=1920:1080:force_original_aspect_ratio=decrease,"
                                f"pad=1920:1080:(ow-iw)/2:(oh-ih)/2,fps=30,setsar=1[v{i}];")

        # Build crossfade chain
        if n == 2:
            offset = durations[0] - td
            filter_parts.append(
                f"[v0][v1]xfade=transition=fade:duration={td}:offset={offset}[outv]"
            )
        else:
            # Chain crossfades for 3+ clips
            offset = durations[0] - td
            filter_parts.append(
                f"[v0][v1]xfade=transition=fade:duration={td}:offset={offset}[xf0];")
            for i in range(2, n):
                prev = f"xf{i-2}"
                offset += durations[i-1] - td
                if i == n - 1:
                    filter_parts.append(
                        f"[{prev}][v{i}]xfade=transition=fade:duration={td}:offset={offset}[outv]")
                else:
                    filter_parts.append(
                        f"[{prev}][v{i}]xfade=transition=fade:duration={td}:offset={offset}[xf{i-1}];")

        filter_str = "".join(filter_parts)

        cmd_str = (
            f"{ffmpeg} -y {inputs} "
            f'-filter_complex "{filter_str}" '
            f"-map [outv] -c:v libx264 -preset medium -crf 18 -pix_fmt yuv420p "
            f"{output_path}"
        )

        print(f"[Compose] Concatenating {len(clips)} clips with crossfade ({td}s)...")
        result = subprocess.run(cmd_str, shell=True, capture_output=True, text=True, timeout=300)

        if result.returncode != 0:
            print(f"[Compose] Crossfade failed, falling back to simple concat", file=sys.stderr)
            return concatenate_clips(clips, output_path, transition="none")

    print(f"[Compose] Output: {output_path}")
    return output_path


def add_audio(
    video_path: str,
    audio_path: str,
    output_path: str,
    volume: float = 1.0,
    replace: bool = False,
) -> str:
    """Add audio track to video."""
    ffmpeg = get_ffmpeg()

    if replace:
        # Replace original audio entirely
        cmd = [
            ffmpeg, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-map", "0:v:0",
            "-map", "1:a:0",
            "-shortest",
            output_path,
        ]
    else:
        # Mix with existing audio
        cmd = [
            ffmpeg, "-y",
            "-i", video_path,
            "-i", audio_path,
            "-c:v", "copy",
            "-filter_complex",
            f"[1:a]volume={volume}[a1];[0:a][a1]amix=inputs=2:duration=first[aout]",
            "-map", "0:v:0",
            "-map", "[aout]",
            output_path,
        ]

    print(f"[Compose] Adding audio to video...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        # If mixing fails (no existing audio), try replacing
        if not replace:
            print("[Compose] Mixing failed (no existing audio?), replacing instead...", file=sys.stderr)
            return add_audio(video_path, audio_path, output_path, volume, replace=True)
        raise RuntimeError(f"FFmpeg audio failed: {result.stderr[-500:]}")

    print(f"[Compose] Output: {output_path}")
    return output_path


def add_music(
    video_path: str,
    music_path: str,
    output_path: str,
    music_volume: float = 0.15,
) -> str:
    """Add background music at low volume (ducked under narration)."""
    ffmpeg = get_ffmpeg()

    cmd = [
        ffmpeg, "-y",
        "-i", video_path,
        "-i", music_path,
        "-filter_complex",
        f"[1:a]volume={music_volume},afade=t=in:d=2,afade=t=out:st=-3:d=3[music];"
        f"[0:a][music]amix=inputs=2:duration=first:dropout_transition=3[aout]",
        "-map", "0:v:0",
        "-map", "[aout]",
        "-c:v", "copy",
        output_path,
    ]

    print(f"[Compose] Adding background music (volume={music_volume})...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg music failed: {result.stderr[-500:]}")

    print(f"[Compose] Output: {output_path}")
    return output_path


def create_title_card(
    text: str,
    output_path: str,
    subtitle: str = "",
    duration: float = 4.0,
    width: int = 1920,
    height: int = 1080,
    bg_color: str = "0x0D1B2A",  # Dark navy
    text_color: str = "white",
    font_size: int = 72,
) -> str:
    """Create a title card video clip."""
    ffmpeg = get_ffmpeg()

    # Build drawtext filter
    drawtext = (
        f"drawtext=text='{text}':fontsize={font_size}:fontcolor={text_color}"
        f":x=(w-text_w)/2:y=(h-text_h)/2-40"
        f":font=Arial"
    )

    if subtitle:
        drawtext += (
            f",drawtext=text='{subtitle}':fontsize={int(font_size*0.5)}"
            f":fontcolor=0xCCCCCC:x=(w-text_w)/2:y=(h-text_h)/2+60"
            f":font=Arial"
        )

    cmd = [
        ffmpeg, "-y",
        "-f", "lavfi",
        "-i", f"color=c={bg_color}:s={width}x{height}:d={duration}:r=30",
        "-vf", drawtext,
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        "-pix_fmt", "yuv420p",
        "-t", str(duration),
        output_path,
    ]

    print(f"[Compose] Creating title card: '{text}'...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=60)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg title card failed: {result.stderr[-500:]}")

    print(f"[Compose] Title card: {output_path}")
    return output_path


def add_subtitles(video_path: str, srt_path: str, output_path: str) -> str:
    """Burn subtitles from SRT file into video."""
    ffmpeg = get_ffmpeg()

    cmd = [
        ffmpeg, "-y",
        "-i", video_path,
        "-vf", f"subtitles={srt_path}:force_style='FontSize=24,PrimaryColour=&Hffffff,OutlineColour=&H000000,Outline=2'",
        "-c:a", "copy",
        "-c:v", "libx264",
        "-preset", "medium",
        "-crf", "18",
        output_path,
    ]

    print(f"[Compose] Burning subtitles from {srt_path}...")
    result = subprocess.run(cmd, capture_output=True, text=True, timeout=300)

    if result.returncode != 0:
        raise RuntimeError(f"FFmpeg subtitles failed: {result.stderr[-500:]}")

    print(f"[Compose] Output: {output_path}")
    return output_path


def create_image_slideshow(
    images: list,
    output_path: str,
    duration_per_image: float = 4.0,
    transition_duration: float = 0.5,
    width: int = 1920,
    height: int = 1080,
) -> str:
    """Create a slideshow video from a list of images with crossfade transitions."""
    ffmpeg = get_ffmpeg()

    # First create individual clips from each image
    temp_clips = []
    for i, img in enumerate(images):
        temp_clip = os.path.join(tempfile.gettempdir(), f"slide_{i}.mp4")
        cmd = [
            ffmpeg, "-y",
            "-loop", "1", "-i", img,
            "-vf", f"scale={width}:{height}:force_original_aspect_ratio=decrease,"
                   f"pad={width}:{height}:(ow-iw)/2:(oh-ih)/2,fps=30",
            "-c:v", "libx264", "-preset", "medium", "-crf", "18",
            "-t", str(duration_per_image),
            "-pix_fmt", "yuv420p",
            temp_clip,
        ]
        subprocess.run(cmd, capture_output=True, text=True, timeout=60)
        temp_clips.append(temp_clip)

    # Concatenate with crossfades
    result = concatenate_clips(temp_clips, output_path, "crossfade", transition_duration)

    # Clean up temp files
    for tc in temp_clips:
        try:
            os.unlink(tc)
        except OSError:
            pass

    return result


# --- Preset compositions ---
PRESETS = {
    "elevator-30s": {
        "description": "30-second elevator pitch with title + clips + closing",
        "steps": [
            {"action": "title", "text": "4.5 millones", "subtitle": "de personas no acceden a sus derechos", "duration": 4},
            {"action": "slideshow", "images_glob": "design/mockups/v3-*.png", "duration_per": 3},
            {"action": "title", "text": "Tu voz tiene poder", "subtitle": "Clara | OdiseIA4Good 2026", "duration": 4},
        ],
    },
    "demo-90s": {
        "description": "90-second demo video structure",
        "steps": [
            {"action": "title", "text": "Clara", "subtitle": "Tu voz tiene poder", "duration": 3},
            {"action": "title", "text": "10 millones de inmigrantes", "subtitle": "67% enfrentan barreras burocraticas", "duration": 4},
            {"action": "slideshow", "images_glob": "design/mockups/v3-*.png", "duration_per": 5},
            {"action": "title", "text": "Open source. Gratis. Siempre.", "subtitle": "github.com/civicaid-voice", "duration": 4},
            {"action": "title", "text": "Tu voz tiene poder", "subtitle": "Clara | OdiseIA4Good 2026 | UDIT Madrid", "duration": 5},
        ],
    },
}


def main():
    parser = argparse.ArgumentParser(
        description="Compose video from clips, audio, and effects",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog=__doc__,
    )

    # Input sources
    parser.add_argument("--clips", nargs="+", help="Video clips to concatenate")
    parser.add_argument("--images", nargs="+", help="Images for slideshow")
    parser.add_argument("--video", help="Base video file")
    parser.add_argument("--audio", help="Voiceover audio to add")
    parser.add_argument("--music", help="Background music to add")
    parser.add_argument("--srt", help="SRT subtitle file")

    # Title card
    parser.add_argument("--title", help="Title card text")
    parser.add_argument("--subtitle", default="", help="Title card subtitle")
    parser.add_argument("--title-duration", type=float, default=4.0, help="Title card duration (seconds)")

    # Output
    parser.add_argument("-o", "--output", required=True, help="Output video path")

    # Settings
    parser.add_argument("--transition", choices=["none", "crossfade"], default="crossfade",
                        help="Transition type between clips")
    parser.add_argument("--transition-duration", type=float, default=0.5,
                        help="Transition duration in seconds")
    parser.add_argument("--music-volume", type=float, default=0.15,
                        help="Background music volume (0.0-1.0)")

    # Preset
    parser.add_argument("--preset", choices=list(PRESETS.keys()), help="Use a predefined composition")
    parser.add_argument("--list-presets", action="store_true", help="List available presets")

    args = parser.parse_args()

    if args.list_presets:
        print("\nAvailable composition presets:\n")
        for name, cfg in PRESETS.items():
            print(f"  {name}: {cfg['description']}")
            for step in cfg["steps"]:
                print(f"    - {step['action']}: {step.get('text', step.get('images_glob', ''))}")
            print()
        return

    Path(args.output).parent.mkdir(parents=True, exist_ok=True)

    # Handle preset
    if args.preset:
        project_root = Path(__file__).resolve().parent.parent.parent
        preset = PRESETS[args.preset]
        print(f"\n[Compose] Building preset: {args.preset}")
        print(f"[Compose] {preset['description']}\n")

        temp_clips = []
        for i, step in enumerate(preset["steps"]):
            temp_path = os.path.join(tempfile.gettempdir(), f"preset_step_{i}.mp4")

            if step["action"] == "title":
                create_title_card(step["text"], temp_path,
                                  subtitle=step.get("subtitle", ""),
                                  duration=step.get("duration", 4))
                temp_clips.append(temp_path)

            elif step["action"] == "slideshow":
                import glob
                pattern = str(project_root / step["images_glob"])
                images = sorted(glob.glob(pattern))
                if images:
                    create_image_slideshow(images, temp_path,
                                           duration_per_image=step.get("duration_per", 4))
                    temp_clips.append(temp_path)
                else:
                    print(f"[Compose] Warning: no images found for {pattern}", file=sys.stderr)

        if temp_clips:
            concatenate_clips(temp_clips, args.output, args.transition, args.transition_duration)
            # Clean up
            for tc in temp_clips:
                try:
                    os.unlink(tc)
                except OSError:
                    pass
        return

    # Manual composition
    current_video = None

    # Step 1: Create title card if requested
    if args.title and not args.clips and not args.video and not args.images:
        create_title_card(args.title, args.output, args.subtitle, args.title_duration)
        return

    # Step 2: Concatenate clips or create slideshow
    if args.clips:
        clips = list(args.clips)
        if args.title:
            title_path = os.path.join(tempfile.gettempdir(), "title_card.mp4")
            create_title_card(args.title, title_path, args.subtitle, args.title_duration)
            clips.insert(0, title_path)
        current_video = os.path.join(tempfile.gettempdir(), "concat_temp.mp4")
        concatenate_clips(clips, current_video, args.transition, args.transition_duration)

    elif args.images:
        current_video = os.path.join(tempfile.gettempdir(), "slideshow_temp.mp4")
        create_image_slideshow(args.images, current_video)

    elif args.video:
        current_video = args.video

    if not current_video:
        print("Error: Provide --clips, --images, --video, or --title", file=sys.stderr)
        sys.exit(1)

    # Step 3: Add voiceover
    if args.audio:
        voiced = os.path.join(tempfile.gettempdir(), "voiced_temp.mp4")
        add_audio(current_video, args.audio, voiced, replace=True)
        current_video = voiced

    # Step 4: Add background music
    if args.music and args.audio:
        musiced = os.path.join(tempfile.gettempdir(), "musiced_temp.mp4")
        add_music(current_video, args.music, musiced, args.music_volume)
        current_video = musiced
    elif args.music:
        musiced = os.path.join(tempfile.gettempdir(), "musiced_temp.mp4")
        add_audio(current_video, args.music, musiced, volume=args.music_volume, replace=True)
        current_video = musiced

    # Step 5: Burn subtitles
    if args.srt:
        subtitled = os.path.join(tempfile.gettempdir(), "subtitled_temp.mp4")
        add_subtitles(current_video, args.srt, subtitled)
        current_video = subtitled

    # Copy final result to output
    if current_video != args.output:
        shutil.copy(current_video, args.output)
        print(f"\n[Compose] Final video: {args.output}")


if __name__ == "__main__":
    main()
