#!/usr/bin/env python3
"""
Ultimate Social Media Video Downloader
Download videos from YouTube, Facebook, Instagram, TikTok
Supports: Single video, Multiple from same platform, Multiple from different platforms (parallel)
"""

import sys
import os
from pathlib import Path
import threading
from queue import Queue
import time
import re
from datetime import datetime

try:
    import yt_dlp
except ImportError:
    print("Error: yt-dlp is not installed.")
    print("Install it using: pip install yt-dlp")
    sys.exit(1)


def safe_title(title, max_words=8, max_length=60):
    """Create a safe shortened title."""
    title = re.sub(r'[^\w\s-]', '', title)
    words = title.split()
    short = ' '.join(words[:max_words])
    return short[:max_length]


def timestamp_name():
    """Return formatted date-time string: DD-MM-YYYY-HH-MM"""
    return datetime.now().strftime("%d-%m-%Y-%H-%M")


class UltimateDownloader:
    def __init__(self, download_path="downloads"):
        self.download_path = Path(download_path)
        self.download_path.mkdir(exist_ok=True)
        self.results = {}
        self.lock = threading.Lock()
        
    def detect_platform(self, url):
        url = url.lower()
        if 'youtube.com' in url or 'youtu.be' in url:
            return 'YouTube'
        elif 'facebook.com' in url or 'fb.watch' in url or 'fb.com' in url:
            return 'Facebook'
        elif 'instagram.com' in url:
            return 'Instagram'
        elif 'tiktok.com' in url:
            return 'TikTok'
        else:
            return 'Unknown'
    
    def progress_hook(self, d, video_id=""):
        if d['status'] == 'downloading':
            downloaded = d.get('downloaded_bytes', 0)
            total = d.get('total_bytes') or d.get('total_bytes_estimate', 0)
            speed = d.get('speed', 0)
            eta = d.get('eta', 0)
            
            if total > 0:
                percent = (downloaded / total) * 100
                downloaded_mb = downloaded / (1024 * 1024)
                total_mb = total / (1024 * 1024)
                speed_mb = (speed / (1024 * 1024)) if speed else 0
                
                prefix = f"[{video_id}] " if video_id else ""
                
                with self.lock:
                    print(f"\r{prefix}Downloading: {percent:.1f}% | "
                          f"{downloaded_mb:.1f}MB / {total_mb:.1f}MB | "
                          f"Speed: {speed_mb:.2f}MB/s | "
                          f"ETA: {eta}s", end='', flush=True)
        elif d['status'] == 'finished':
            prefix = f"[{video_id}] " if video_id else ""
            with self.lock:
                print(f"\n{prefix}✓ Download completed! Processing...")

    def download_single(self, url):
        platform = self.detect_platform(url)
        
        print(f"\n{'='*60}")
        print(f"📹 Single Video Download - {platform}")
        print(f"{'='*60}")
        
        try:
            filename = f"{timestamp_name()}.%(ext)s"

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': str(self.download_path / filename),
                'progress_hooks': [self.progress_hook],
                'merge_output_format': 'mp4',
            }
            
            print("Starting download...")

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            print(f"\n✅ Video downloaded successfully!")
            print(f"📁 Filename: {timestamp_name()}.mp4")
            print(f"📂 Saved to: {self.download_path.absolute()}")
            return True

        except Exception as e:
            print(f"\n❌ Error: {str(e)}")
            return False

    def download_batch_same_platform(self, urls):
        if not urls:
            print("❌ No URLs provided")
            return
        
        urls = [url.strip() for url in urls if url.strip()]
        platform = self.detect_platform(urls[0])
        
        print(f"\n{'='*60}")
        print(f"📦 Batch Download - {platform}")
        print(f"{'='*60}")
        print(f"Total videos: {len(urls)}")
        print(f"Platform: {platform}")
        print(f"{'='*60}\n")
        
        success_count = 0
        start_time = time.time()
        
        for i, url in enumerate(urls, 1):
            print(f"\n{'='*60}")
            print(f"📹 Downloading {i}/{len(urls)}")
            print(f"{'='*60}")
            
            if self.download_single(url):
                success_count += 1
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*60}")
        print("📊 BATCH SUMMARY")
        print(f"{'='*60}")
        print(f"✅ Successful: {success_count}/{len(urls)}")
        print(f"❌ Failed: {len(urls) - success_count}/{len(urls)}")
        print(f"⏱️  Total time: {elapsed_time:.1f}s")
        print(f"📁 Location: {self.download_path.absolute()}")
        print(f"{'='*60}\n")
    
    def download_worker(self, url, url_id):
        platform = self.detect_platform(url)
        
        try:
            with self.lock:
                print(f"\n[{url_id}] 🚀 Starting download from {platform}")
            
            filename = f"[{url_id}] {timestamp_name()}.%(ext)s"

            ydl_opts = {
                'format': 'bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best',
                'outtmpl': str(self.download_path / filename),
                'progress_hooks': [lambda d: self.progress_hook(d, url_id)],
                'merge_output_format': 'mp4',
                'quiet': True,
                'no_warnings': True,
            }

            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                ydl.download([url])

            with self.lock:
                print(f"\n[{url_id}] ✅ SUCCESS - {platform} video downloaded!")

        except Exception as e:
            with self.lock:
                print(f"\n[{url_id}] ❌ ERROR: {str(e)[:100]}")

    def download_parallel_multi_platform(self, urls, max_workers=3):
        if not urls:
            print("❌ No URLs provided")
            return
        
        urls = [url.strip() for url in urls if url.strip()]
        urls = list(dict.fromkeys(urls))
        
        print(f"\n{'='*70}")
        print(f"⚡ PARALLEL MULTI-PLATFORM DOWNLOAD")
        print(f"{'='*70}")
        print(f"📊 Total videos: {len(urls)}")
        print(f"⚡ Parallel threads: {min(max_workers, len(urls))}")
        print(f"📁 Download folder: {self.download_path.absolute()}")
        print(f"{'='*70}\n")
        
        for i, url in enumerate(urls, 1):
            platform = self.detect_platform(url)
            print(f"[{i}] {platform}: {url[:60]}...")
        
        print(f"\n{'='*70}")
        print("Starting parallel downloads...")
        print(f"{'='*70}\n")
        
        start_time = time.time()
        threads = []
        
        for i, url in enumerate(urls, 1):
            thread = threading.Thread(target=self.download_worker, args=(url, i), daemon=True)
            thread.start()
            threads.append(thread)
            
            if len(threads) >= max_workers:
                threads[0].join()
                threads.pop(0)
        
        for thread in threads:
            thread.join()
        
        elapsed_time = time.time() - start_time
        
        print(f"\n{'='*70}")
        print("📊 DOWNLOAD SUMMARY")
        print(f"{'='*70}")
        
        print(f"⏱️  Total time: {elapsed_time:.1f}s")
        print(f"📁 Location: {self.download_path.absolute()}")
        print(f"{'='*70}\n")


def main():
    print("="*70)
    print("Ultimate Social Media Video Downloader".center(70))
    print("YouTube • Facebook • Instagram • TikTok".center(70))
    print("="*70)
    
    downloader = UltimateDownloader()
    
    print(f"\n📁 Download folder: {downloader.download_path.absolute()}\n")
    
    while True:
        try:
            print("\n" + "="*70)
            print("SELECT DOWNLOAD MODE:")
            print("="*70)
            print("  1. 📹 Download single video")
            print("  2. 📦 Download multiple videos from SAME platform (batch)")
            print("  3. ⚡ Download multiple videos from DIFFERENT platforms (parallel)")
            print("  4. ❌ Quit")
            print("="*70)
            
            choice = input("\nSelect option (1-4): ").strip()
            
            if choice == '1':
                print("\n" + "="*70)
                print("📹 SINGLE VIDEO DOWNLOAD")
                print("="*70)
                url = input("\nEnter video URL: ").strip()
                
                if not url:
                    print("❌ Please enter a valid URL")
                    continue
                
                if not url.startswith(('http://', 'https://')):
                    print("❌ URL must start with http:// or https://")
                    continue
                
                platform = downloader.detect_platform(url)
                print(f"✓ Platform detected: {platform}")
                
                downloader.download_single(url)
            
            elif choice == '2':
                print("\n" + "="*70)
                print("📦 BATCH DOWNLOAD - SAME PLATFORM")
                print("="*70)

                print("\nEnter URLs one by one.")
                print("➡ Press Enter after each URL")
                print("➡ Press Enter AGAIN on empty line to start downloading\n")

                urls = []
                while True:
                    url = input("🔗 URL: ").strip()
                    if url == "":
                        break
                    if not url.startswith(('http://', 'https://')):
                        print("❌ Invalid URL. Must start with http:// or https://")
                        continue
                    urls.append(url)
                    platform = downloader.detect_platform(url)
                    print(f"   ✅ Added: {platform}")

                if not urls:
                    print("❌ No URLs entered")
                    continue

                print(f"\n🚀 Starting download for {len(urls)} URLs...\n")
                downloader.download_batch_same_platform(urls)
            
            elif choice == '3':
                print("\n" + "="*70)
                print("⚡ PARALLEL MULTI-PLATFORM DOWNLOAD")
                print("="*70)
                
                max_workers_input = input("\nHow many parallel downloads? (1-5, default=3): ").strip()
                try:
                    max_workers = int(max_workers_input) if max_workers_input else 3
                    max_workers = max(1, min(5, max_workers))
                except:
                    max_workers = 3
                
                print(f"✅ Parallel downloads: {max_workers}")

                print("\nEnter URLs one by one.")
                print("➡ Press Enter after each URL")
                print("➡ Press Enter AGAIN on empty line to start downloading\n")

                urls = []
                while True:
                    url = input("🔗 URL: ").strip()
                    if url == "":
                        break
                    if not url.startswith(('http://', 'https://')):
                        print("❌ Invalid URL. Must start with http:// or https://")
                        continue
                    urls.append(url)
                    platform = downloader.detect_platform(url)
                    print(f"   ✅ Added: {platform}")

                if not urls:
                    print("❌ No URLs entered")
                    continue

                print(f"\n🚀 Starting download for {len(urls)} URLs...\n")
                downloader.download_parallel_multi_platform(urls, max_workers)
            
            elif choice == '4' or choice.lower() in ['q', 'quit', 'exit']:
                print("\n👋 Goodbye!")
                break
            
            else:
                print("❌ Invalid option. Please select 1-4.")
        
        except KeyboardInterrupt:
            print("\n\n👋 Interrupted. Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    main()
