#!/usr/bin/env python3
"""
Ultra-Fast TikTok Video Converter
Maximum speed conversion with progress bar
"""

import sys
import os
from pathlib import Path
import subprocess
import re


def check_ffmpeg():
    try:
        result = subprocess.run(['ffmpeg', '-version'],
                              capture_output=True,
                              text=True,
                              timeout=5)
        return result.returncode == 0
    except (FileNotFoundError, subprocess.TimeoutExpired):
        return False


def get_duration(input_file):
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-show_entries', 'format=duration',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            return float(result.stdout.strip())
    except:
        pass
    return None


def get_video_resolution(input_file):
    try:
        cmd = [
            'ffprobe', '-v', 'error',
            '-select_streams', 'v:0',
            '-show_entries', 'stream=width,height',
            '-of', 'default=noprint_wrappers=1:nokey=1',
            input_file
        ]
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=10)
        if result.returncode == 0:
            lines = result.stdout.strip().split('\n')
            if len(lines) >= 2:
                width = int(lines[0])
                height = int(lines[1])
                return width, height
    except:
        pass
    return None, None


def convert_ultrafast(input_file, output_file=None):
    input_path = Path(input_file)

    if not input_path.exists():
        print(f"❌ File not found: {input_file}")
        return False

    # ✅ ADDED: Converted folder logic (only change)
    converted_dir = input_path.parent / "Converted"
    converted_dir.mkdir(exist_ok=True)

    if output_file is None:
        output_file = converted_dir / f"{input_path.stem}_tiktok.mp4"
    else:
        output_file = Path(output_file)

    print(f"\n{'='*60}")
    print(f"🚀 ULTRA-FAST TikTok Converter (1080p)")
    print(f"{'='*60}")
    print(f"📥 Input:  {input_path.name}")
    print(f"📤 Output: {output_file.name}")

    duration = get_duration(str(input_path))
    width, height = get_video_resolution(str(input_path))

    if duration:
        print(f"⏱️  Duration: {duration:.1f}s")

    if width and height:
        print(f"📐 Original Resolution: {width}x{height}")

        if height < 1080:
            print(f"⬆️  Action: Upscaling to 1080p")
        elif height > 1080:
            print(f"⬇️  Action: Downscaling to 1080p")
        else:
            print(f"✓  Action: Already 1080p - optimizing format")

    print(f"🎯 Target: 1080p (1920x1080)")
    print(f"\n🔄 Converting... (This should be FAST!)")
    print(f"{'='*60}\n")

    cmd = [
        'ffmpeg',
        '-i', str(input_path),
        '-vf', 'scale=-2:1080',
        '-c:v', 'libx264',
        '-preset', 'ultrafast',
        '-crf', '23',
        '-profile:v', 'main',
        '-level', '4.0',
        '-pix_fmt', 'yuv420p',
        '-r', '30',
        '-g', '60',
        '-c:a', 'aac',
        '-b:a', '128k',
        '-ar', '44100',
        '-movflags', '+faststart',
        '-f', 'mp4',
        '-progress', 'pipe:1',
        '-loglevel', 'error',
        '-y',
        str(output_file)
    ]

    try:
        start_time = time.time()

        process = subprocess.Popen(
            cmd,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            universal_newlines=True,
            bufsize=1
        )

        last_progress = 0
        for line in process.stdout:
            if line.startswith('out_time_ms='):
                try:
                    time_value = line.split('=')[1].strip()
                    if not time_value or time_value == 'N/A':
                        continue

                    clean_value = time_value.replace('-', '')
                    if not clean_value.isdigit():
                        continue

                    time_ms = int(time_value)
                    if time_ms <= 0:
                        continue

                    current_time = time_ms / 1000000.0

                    if duration and duration > 0:
                        progress = (current_time / duration) * 100
                        progress = min(progress, 100)

                        if abs(progress - last_progress) >= 1:
                            bar_length = 40
                            filled = int(bar_length * progress / 100)
                            bar = '█' * filled + '░' * (bar_length - filled)

                            print(f'\r[{bar}] {progress:.1f}% | {current_time:.1f}s / {duration:.1f}s',
                                  end='', flush=True)
                            last_progress = progress
                except:
                    pass

        process.wait()

        if process.returncode == 0:
            elapsed = time.time() - start_time
            output_size = output_file.stat().st_size / (1024 * 1024)

            print(f"\n\n{'='*60}")
            print(f"✅ SUCCESS! Conversion Complete!")
            print(f"{'='*60}")
            print(f"📁 File: {output_file.name}")
            print(f"💾 Size: {output_size:.2f} MB")
            print(f"⏱️  Time: {elapsed:.1f}s")
            print(f"📍 Path: {output_file.absolute()}")
            print(f"\n✨ Ready for TikTok/CapCut/Instagram!")
            print(f"{'='*60}\n")
            return True
        else:
            stderr_output = process.stderr.read()
            print(f"\n❌ Conversion failed!")
            print(f"Error: {stderr_output}")
            return False

    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        return False


def batch_convert(input_dir):
    input_path = Path(input_dir)

    if not input_path.is_dir():
        print(f"❌ Not a directory: {input_dir}")
        return

    video_exts = ['.mp4', '.mov', '.avi', '.mkv', '.flv', '.wmv', '.webm', '.m4v']

    videos = []
    for ext in video_exts:
        videos.extend(input_path.glob(f'*{ext}'))
        videos.extend(input_path.glob(f'*{ext.upper()}'))

    if not videos:
        print(f"❌ No videos found in {input_dir}")
        return

    print(f"\n🎬 Found {len(videos)} video(s)\n")

    success = 0
    for i, video in enumerate(videos, 1):
        print(f"\n{'='*60}")
        print(f"📹 Processing {i}/{len(videos)}")
        print(f"{'='*60}")

        if convert_ultrafast(str(video)):
            success += 1

    print(f"\n{'='*60}")
    print(f"🎉 Batch Complete: {success}/{len(videos)} successful")
    print(f"{'='*60}\n")


def main():
    print("="*60)
    print("🚀 ULTRA-FAST TikTok Video Converter".center(60))
    print("Maximum speed - Good quality".center(60))
    print("="*60)

    if not check_ffmpeg():
        print("\n❌ FFmpeg not installed!")
        print("\n📦 Install: pkg install ffmpeg")
        sys.exit(1)

    print("\n✅ FFmpeg ready\n")

    while True:
        print("\n" + "="*60)
        print("Options:")
        print("  1. Convert single video (FAST)")
        print("  2. Convert folder (batch)")
        print("  3. Quit")
        print("="*60)

        choice = input("\nSelect (1-3): ").strip()

        if choice == '1':
            path = input("\n📂 Video path: ").strip()
            if path:
                convert_ultrafast(path)

        elif choice == '2':
            path = input("\n📂 Folder path: ").strip()
            if path:
                batch_convert(path)

        elif choice == '3':
            break

        else:
            print("❌ Invalid option")


if __name__ == "__main__":
    try:
        import time
        main()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted. Bye!")
        sys.exit(0)
