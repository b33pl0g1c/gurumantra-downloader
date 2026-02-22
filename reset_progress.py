"""
Utility: Reset all downloaded flags to False.
Run this ONCE before sending the folder to someone else,
so their copy starts fresh with no videos marked as downloaded.

Usage:  python reset_progress.py
"""
import json, os

path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "video_list.json")
with open(path, "r", encoding="utf-8") as f:
    videos = json.load(f)

for v in videos:
    v["downloaded"] = False

with open(path, "w", encoding="utf-8") as f:
    json.dump(videos, f, indent=2, ensure_ascii=False)

count = len(videos)
print(f"✅ Reset complete! All {count} videos marked as NOT downloaded.")
print(f"   The recipient can now double-click DOWNLOAD_VIDEOS.bat to start fresh.")
