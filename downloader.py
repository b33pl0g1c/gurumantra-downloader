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
import subprocess
import sys


# ─── Configuration ───────────────────────────────────────────────────────────
VIDEO_LIST_FILE = "video_list.json"   # Contains all 139 video details + YouTube IDs
DOWNLOAD_DIR = "downloads"


def check_requirements():
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


def download_all_videos():
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
            "--no-warnings",
            "-f", "bestvideo[ext=mp4]+bestaudio[ext=m4a]/best[ext=mp4]/best",
            "--merge-output-format", "mp4",
            "-o", os.path.join(download_dir, "%(title)s [%(id)s].%(ext)s"),
            "--no-overwrites",
            "--retries", "3",
            "--fragment-retries", "3",
            "--concurrent-fragments", "4",
            yt_url,
        ]

        try:
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=600)

            if result.returncode == 0:
                print(f"   ✅ Downloaded successfully!")
                video["downloaded"] = True
                success_count += 1
            else:
                stdout = result.stdout.strip()
                stderr = result.stderr.strip()
                if "has already been downloaded" in stdout or "has already been recorded" in stdout:
                    print(f"   ✅ Already downloaded, skipping.")
                    video["downloaded"] = True
                    success_count += 1
                else:
                    error_msg = stderr[:200] if stderr else stdout[:200]
                    print(f"   ❌ Failed: {error_msg}")
                    fail_count += 1

        except subprocess.TimeoutExpired:
            print(f"   ⏰ Timed out after 10 minutes, skipping...")
            fail_count += 1
        except FileNotFoundError:
            print("   ❌ yt-dlp not found! Try running: pip install yt-dlp")
            input("\nPress Enter to exit...")
            return
        except Exception as e:
            print(f"   ❌ Error: {e}")
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

    # Step 1: Check requirements
    if not check_requirements():
        input("\nPress Enter to exit...")
        sys.exit(1)

    # Step 2: Download all videos
    download_all_videos()
