# Ultimate Social Media Video Downloader

**All-in-one video downloader** with 3 download modes for YouTube, Facebook, Instagram, and TikTok!

## 🎯 Three Download Modes

### 1. 📹 Single Video Download
- Download one video at a time
- See detailed info before download
- Best for: Quick single downloads

### 2. 📦 Batch Download (Same Platform)
- Download multiple videos from ONE platform
- Sequential downloads (one after another)
- Best for: YouTube playlists, Instagram profile downloads

### 3. ⚡ Parallel Download (Multi-Platform)
- Download from DIFFERENT platforms simultaneously
- 3-5 videos at the same time
- Best for: Bulk downloads from mixed platforms

## Supported Platforms

| Platform | Content Types | Quality |
|----------|--------------|---------|
| 📺 **YouTube** | Videos, Shorts | Up to 8K |
| 📘 **Facebook** | Videos, Watch | HD |
| 📷 **Instagram** | Posts, Reels, Stories | Original |
| 🎵 **TikTok** | Videos | HD (no watermark) |

## Installation

```bash
# Install yt-dlp
pip install yt-dlp

# Install FFmpeg (required)
pkg install ffmpeg  # Termux
sudo apt install ffmpeg  # Ubuntu
brew install ffmpeg  # macOS
```

## Usage

### Run the script:

```bash
python ultimate_downloader.py
```

## Mode 1: Single Video Download

**Use when:** You need to download just one video

```
SELECT DOWNLOAD MODE:
======================================================================
  1. 📹 Download single video
  2. 📦 Download multiple videos from SAME platform (batch)
  3. ⚡ Download multiple videos from DIFFERENT platforms (parallel)
  4. ❌ Quit
======================================================================

Select option (1-4): 1

======================================================================
📹 SINGLE VIDEO DOWNLOAD
======================================================================

Enter video URL: https://youtube.com/watch?v=abc123
✓ Platform detected: YouTube

============================================================
📹 Single Video Download - YouTube
============================================================
Fetching video information...
Title: Amazing Video Title
Duration: 5m 23s
Quality: 1080p
Size: ~125.4MB

Starting download...
Downloading: 45.2% | 56.7MB / 125.4MB | Speed: 8.45MB/s | ETA: 8s
✓ Download completed! Processing...

✅ Video downloaded successfully!
Saved to: /path/to/downloads
```

**Features:**
- ✅ Shows video info before download
- ✅ Real-time progress tracking
- ✅ Quality and size display
- ✅ Automatic format detection

---

## Mode 2: Batch Download (Same Platform)

**Use when:** Downloading multiple videos from ONE platform (e.g., 5 YouTube videos)

```
Select option (1-4): 2

======================================================================
📦 BATCH DOWNLOAD - SAME PLATFORM
======================================================================
Enter multiple URLs from the SAME platform
Press Enter on empty line when done
======================================================================

URL 1 (or Enter to start): https://youtube.com/watch?v=video1
   ✓ Added: YouTube
URL 2 (or Enter to start): https://youtube.com/watch?v=video2
   ✓ Added: YouTube
URL 3 (or Enter to start): https://youtube.com/watch?v=video3
   ✓ Added: YouTube
URL 4 (or Enter to start): 

============================================================
📦 Batch Download - YouTube
============================================================
Total videos: 3
Platform: YouTube
============================================================

============================================================
📹 Downloading 1/3
============================================================
[Downloads video 1...]

============================================================
📹 Downloading 2/3
============================================================
[Downloads video 2...]

============================================================
📹 Downloading 3/3
============================================================
[Downloads video 3...]

============================================================
📊 BATCH SUMMARY
============================================================
✅ Successful: 3/3
❌ Failed: 0/3
⏱️  Total time: 245.7s
📁 Location: /path/to/downloads
============================================================
```

**Features:**
- ✅ Downloads one after another
- ✅ Progress for each video
- ✅ Final summary with stats
- ✅ Best for same-platform bulk downloads

---

## Mode 3: Parallel Download (Multi-Platform)

**Use when:** Downloading from DIFFERENT platforms simultaneously (YouTube + Instagram + TikTok)

```
Select option (1-4): 3

======================================================================
⚡ PARALLEL MULTI-PLATFORM DOWNLOAD
======================================================================

How many parallel downloads? (1-5, default=3): 3
✅ Parallel downloads: 3

======================================================================
Enter video URLs from ANY platform
Press Enter on empty line when done
======================================================================

URL 1 (or Enter to start): https://youtube.com/watch?v=abc123
   ✓ Added: YouTube
URL 2 (or Enter to start): https://instagram.com/p/xyz789/
   ✓ Added: Instagram
URL 3 (or Enter to start): https://tiktok.com/@user/video/123
   ✓ Added: TikTok
URL 4 (or Enter to start): https://facebook.com/video/456
   ✓ Added: Facebook
URL 5 (or Enter to start): 

======================================================================
⚡ PARALLEL MULTI-PLATFORM DOWNLOAD
======================================================================
📊 Total videos: 4
⚡ Parallel threads: 3
📁 Download folder: /path/to/downloads
======================================================================

[1] YouTube: https://youtube.com/watch?v=abc123...
[2] Instagram: https://instagram.com/p/xyz789/...
[3] TikTok: https://tiktok.com/@user/video/123...
[4] Facebook: https://facebook.com/video/456...

======================================================================
Starting parallel downloads...
======================================================================

[1] 🚀 Starting download from YouTube
[1] 📹 Amazing YouTube Video...
[1] ⏱️  Duration: 5m 23s

[2] 🚀 Starting download from Instagram
[2] 📹 Cool Instagram Reel...
[2] ⏱️  Duration: 0m 45s

[3] 🚀 Starting download from TikTok
[3] 📹 Funny TikTok...
[3] ⏱️  Duration: 0m 30s

[1] Downloading: 15.3% | 5.2/34.1MB | Speed: 2.34MB/s | ETA: 12s
[2] Downloading: 42.7% | 3.1/7.2MB | Speed: 1.89MB/s | ETA: 2s
[3] Downloading: 68.9% | 4.5/6.5MB | Speed: 3.12MB/s | ETA: 1s

[3] ✓ Download completed! Processing...
[3] ✅ SUCCESS - TikTok video downloaded!

[4] 🚀 Starting download from Facebook
...

======================================================================
📊 DOWNLOAD SUMMARY
======================================================================
✅ Successful: 4/4
❌ Failed: 0/4
⏱️  Total time: 145.3s
📁 Location: /path/to/downloads
======================================================================
```

**Features:**
- ✅ **3-5 videos download at once**
- ✅ Mix platforms freely
- ✅ 3-5x faster than sequential
- ✅ Live progress for each download
- ✅ Numbers in filenames for easy identification

---

## Mode Comparison

| Feature | Single | Batch (Same) | Parallel (Multi) |
|---------|--------|--------------|------------------|
| **Speed** | Normal | Sequential | 3-5x faster |
| **Platforms** | Any one | One platform | Mix platforms |
| **Best for** | Quick downloads | YouTube playlists | Bulk mixed downloads |
| **Concurrent** | 1 at a time | 1 at a time | 3-5 at once |
| **Use case** | Single video | 10 YouTube videos | 5 from different platforms |

## When to Use Each Mode

### Use Mode 1 (Single) when:
- ✅ You need just one video
- ✅ Want to see detailed info first
- ✅ Testing a new platform/URL

### Use Mode 2 (Batch Same) when:
- ✅ Downloading from ONE platform only
- ✅ YouTube playlist or channel
- ✅ Multiple Instagram posts from same user
- ✅ Don't need parallel speed

### Use Mode 3 (Parallel Multi) when:
- ✅ Downloading from DIFFERENT platforms
- ✅ Want maximum speed (3-5x faster)
- ✅ Bulk downloads (10+ videos)
- ✅ Mix of YouTube + Instagram + TikTok etc.

## Output Files

### Single & Batch (Same Platform):
```
downloads/
├── Video Title 1.mp4
├── Video Title 2.mp4
└── Video Title 3.mp4
```

### Parallel (Multi-Platform):
```
downloads/
├── [1] YouTube Video.mp4
├── [2] Instagram Reel.mp4
├── [3] TikTok Video.mp4
└── [4] Facebook Video.mp4
```
*Numbers match the URL order you entered*

## Tips

### For Single Downloads:
- Check video info before downloading
- Perfect for one-off downloads

### For Batch (Same Platform):
- Great for YouTube playlists
- Downloads reliably one by one
- No platform rate limiting issues

### For Parallel (Multi-Platform):
- Use 3 parallel for balanced speed
- Use 4-5 if you have fast internet
- Mix platforms freely (YouTube + TikTok + Instagram)
- Much faster for bulk downloads

## Troubleshooting

### "yt-dlp is not installed"
```bash
pip install yt-dlp
```

### "FFmpeg not found"
```bash
pkg install ffmpeg  # Termux
```

### Parallel downloads slow
- Reduce parallel count to 2-3
- Check your internet speed
- Some platforms may rate-limit

### Single platform batch failing
- Try parallel mode instead
- Update yt-dlp: `pip install -U yt-dlp`

## Requirements

- Python 3.6+
- yt-dlp
- FFmpeg
- Stable internet connection

## License

Free to use for personal use.
