"""
╔══════════════════════════════════════════════════════════════╗
║           GuruMantra Video Downloader (Easy Mode)           ║
║                                                              ║
║   Downloads all 139 purchased videos from gurumantrapsc.com  ║
║   Just run this script — it handles everything!              ║
╚══════════════════════════════════════════════════════════════╝
"""

import json
import os
import shutil
import subprocess
import sys


# ─── Configuration ───────────────────────────────────────────────────────────
VIDEO_LIST_FILE = "video_list.json"   # Contains all 139 video details + YouTube IDs
DOWNLOAD_DIR = "downloads"


def pip_install(package):
    """Install a Python package using pip."""
    subprocess.run(
        [sys.executable, "-m", "pip", "install", package],
        capture_output=True, timeout=120
    )


def check_ytdlp():
    """Check that yt-dlp is installed. If not, install it automatically."""
    print("\n🔍 Checking if yt-dlp is installed...")
    try:
        result = subprocess.run(
            [sys.executable, "-m", "yt_dlp", "--version"],
            capture_output=True, text=True, timeout=15
        )
        if result.returncode == 0:
            print(f"   ✅ yt-dlp is installed (version {result.stdout.strip()})")
            return True
    except Exception:
        pass

    # yt-dlp not found, try to install it
    print("   ⚠️  yt-dlp is NOT installed. Installing it now...")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "yt-dlp"],
            check=True, timeout=120
        )
        print("   ✅ yt-dlp installed successfully!")
        return True
    except Exception as e:
        print(f"\n   ❌ ERROR: Could not install yt-dlp: {e}")
        print("   👉 Please run this command manually:")
        print("      pip install yt-dlp")
        return False


def check_ffmpeg():
    """
    Check if ffmpeg is available.
    If not, try to install it automatically via pip (imageio-ffmpeg).
    Returns the path to ffmpeg, or None if unavailable.
    """
    print("🔍 Checking if ffmpeg is installed...")

    # Method 1: Check if ffmpeg is already on system PATH
    ffmpeg_path = shutil.which("ffmpeg")
    if ffmpeg_path:
        print(f"   ✅ ffmpeg found on system: {ffmpeg_path}")
        return ffmpeg_path

    # Method 2: Check if imageio-ffmpeg is already installed
    ffmpeg_path = _get_imageio_ffmpeg()
    if ffmpeg_path:
        print(f"   ✅ ffmpeg found via imageio-ffmpeg")
        return ffmpeg_path

    # Method 3: Try to install imageio-ffmpeg (bundles ffmpeg binary)
    print("   ⚠️  ffmpeg is NOT installed. Installing it now...")
    print("   (This is needed to combine video + audio into one file)")
    try:
        subprocess.run(
            [sys.executable, "-m", "pip", "install", "imageio-ffmpeg"],
            check=True, timeout=180,
            capture_output=True
        )
        ffmpeg_path = _get_imageio_ffmpeg()
        if ffmpeg_path:
            print(f"   ✅ ffmpeg installed successfully via imageio-ffmpeg!")
            return ffmpeg_path
    except Exception:
        pass

    # All methods failed
    print("   ⚠️  Could not install ffmpeg automatically.")
    print("   📥 Videos will be downloaded at 720p (single file, no merge needed).")
    print("   💡 For higher quality, install ffmpeg manually:")
    print("      https://ffmpeg.org/download.html")
    return None


def _get_imageio_ffmpeg():
    """Try to get ffmpeg path from imageio-ffmpeg package."""
    try:
        import imageio_ffmpeg
        path = imageio_ffmpeg.get_ffmpeg_exe()
        if path and os.path.exists(path):
            return path
    except (ImportError, Exception):
        pass
    return None


def download_all_videos(ffmpeg_path=None):
    """Download all 139 videos. Skips already-downloaded ones."""

    # ── Load the video list ──
    script_dir = os.path.dirname(os.path.abspath(__file__))
    video_list_path = os.path.join(script_dir, VIDEO_LIST_FILE)
    download_dir = os.path.join(script_dir, DOWNLOAD_DIR)

    if not os.path.exists(video_list_path):
        print(f"\n❌ ERROR: '{VIDEO_LIST_FILE}' not found!")
        print(f"   Make sure this file is in the same folder as this script.")
        print(f"   Expected location: {video_list_path}")
        input("\nPress Enter to exit...")
        return

    with open(video_list_path, "r", encoding="utf-8") as f:
        videos = json.load(f)

    os.makedirs(download_dir, exist_ok=True)

    # ── Count what needs downloading ──
    total = len(videos)
    valid_videos = [v for v in videos if v.get("youtube_id")]
    already_done = [v for v in valid_videos if v.get("downloaded")]
    to_download = [v for v in valid_videos if not v.get("downloaded")]
    no_id = [v for v in videos if not v.get("youtube_id")]

    # ── Determine download quality based on ffmpeg availability ──
    if ffmpeg_path:
        quality_mode = "HIGH"
        # Download best video + best audio separately, then merge into MP4
        fmt = "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best"
    else:
        quality_mode = "STANDARD"
        # Download pre-merged MP4 (up to 720p, but no ffmpeg needed)
        fmt = "best[ext=mp4]/best"

    # ── Show status ──
    print("\n" + "═" * 60)
    print("📊  VIDEO DOWNLOAD STATUS")
    print("═" * 60)
    print(f"   📁 Total videos:         {total}")
    print(f"   ✅ Already downloaded:    {len(already_done)}")
    print(f"   ⬇️  Remaining to download: {len(to_download)}")
    if no_id:
        print(f"   ⚠️  Missing YouTube ID:   {len(no_id)} (will be skipped)")
    print(f"   📂 Download folder:       {download_dir}")
    if quality_mode == "HIGH":
        print(f"   🎬 Quality:               HIGH (best video + audio, merged)")
    else:
        print(f"   🎬 Quality:               STANDARD (720p, single file)")
    print("═" * 60)

    if not to_download:
        print("\n🎉 All videos are already downloaded! Nothing to do.")
        input("\nPress Enter to exit...")
        return

    print(f"\n🚀 Starting download of {len(to_download)} videos...")
    print("   (You can close this window anytime — progress is saved.)")
    print("   (Just run the script again to resume from where you stopped.)\n")

    # ── Download each video ──
    success_count = 0
    fail_count = 0

    for i, video in enumerate(to_download, 1):
        yt_id = video["youtube_id"]
        title = video.get("title", f"Video {video.get('internal_id', 'unknown')}")
        yt_url = f"https://www.youtube.com/watch?v={yt_id}"

        # Show progress
        progress_pct = round((i / len(to_download)) * 100)
        print(f"\n{'─' * 60}")
        print(f"📥 [{i}/{len(to_download)}] ({progress_pct}% done)")
        print(f"   Title: {title[:70]}")
        print(f"   URL:   {yt_url}")

        # Build yt-dlp command
        cmd = [
            sys.executable, "-m", "yt_dlp",
            "--quiet",               # Suppress all noise
            "--progress",            # But still show progress bar
            "--no-warnings",         # No warning messages
            "-f", fmt,
            "-o", os.path.join(download_dir, "%(title)s [%(id)s].%(ext)s"),
            "--no-overwrites",
            "--retries", "3",
            "--fragment-retries", "3",
            yt_url,
        ]

        # Add merge options only if ffmpeg is available
        if ffmpeg_path:
            cmd.insert(4, "--merge-output-format")
            cmd.insert(5, "mp4")
            cmd.extend(["--ffmpeg-location", os.path.dirname(ffmpeg_path)])
            cmd.extend(["--concurrent-fragments", "4"])

        try:
            # Stream output directly to console (shows live progress)
            result = subprocess.run(cmd, timeout=600)

            if result.returncode == 0:
                print(f"\n   ✅ Downloaded successfully!")
                video["downloaded"] = True
                success_count += 1
            else:
                print(f"\n   ❌ Failed (exit code {result.returncode})")
                fail_count += 1

        except subprocess.TimeoutExpired:
            print(f"\n   ⏰ Timed out after 10 minutes, skipping...")
            fail_count += 1
        except FileNotFoundError:
            print("   ❌ yt-dlp not found! Try running: pip install yt-dlp")
            input("\nPress Enter to exit...")
            return
        except Exception as e:
            print(f"\n   ❌ Error: {e}")
            fail_count += 1

        # Save progress after EVERY video (so you can resume later)
        with open(video_list_path, "w", encoding="utf-8") as f:
            json.dump(videos, f, indent=2, ensure_ascii=False)

    # ── Final summary ──
    print("\n" + "═" * 60)
    print("🏁  DOWNLOAD COMPLETE!")
    print("═" * 60)
    print(f"   ✅ Successfully downloaded: {success_count}")
    if fail_count > 0:
        print(f"   ❌ Failed:                  {fail_count}")
        print(f"   💡 Tip: Run this script again to retry failed downloads.")
    print(f"   📂 Videos saved to: {download_dir}")
    print("═" * 60)

    input("\nPress Enter to exit...")


# ─── Main ────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("╔══════════════════════════════════════════════════════════════╗")
    print("║           GuruMantra Video Downloader (Easy Mode)           ║")
    print("║                                                              ║")
    print("║   This will download all 139 purchased videos.              ║")
    print("║   Videos are saved to the 'downloads' folder.               ║")
    print("║   You can stop and resume anytime — progress is saved!      ║")
    print("╚══════════════════════════════════════════════════════════════╝")

    # Step 1: Check yt-dlp
    if not check_ytdlp():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 2: Check ffmpeg (needed to merge video + audio into single MP4)
    ffmpeg_path = check_ffmpeg()

    # Step 3: Download all videos
    download_all_videos(ffmpeg_path=ffmpeg_path)
