# 📥 GuruMantra Video Downloader

This tool downloads **all 139 purchased videos** from gurumantrapsc.com with just **one double-click**. No technical knowledge required!

---

## 📋 What You Need to Do (Step-by-Step)

### Step 1: Install Python (One-Time Only)

Python is a free program that runs this downloader. You only need to install it once.

1. **Open your web browser** (Chrome, Edge, Firefox — any browser works)

2. **Go to this website:**
   ```
   https://www.python.org/downloads/
   ```
   (You can copy-paste this link into your browser's address bar)

3. **Click the big yellow button** that says **"Download Python 3.x.x"**
   (The exact number doesn't matter — just click the big yellow button)

4. **Wait for the file to download**, then **open/run** the downloaded file
   - It will be named something like `python-3.x.x-amd64.exe`
   - You'll find it in your **Downloads** folder, or at the bottom of your browser

5. ⚠️ **VERY IMPORTANT:** On the first screen of the installer, you will see a checkbox at the bottom that says:
   
   ✅ **"Add Python to PATH"** (or "Add python.exe to PATH")
   
   **YOU MUST CHECK THIS BOX!** This is the most important step. If you miss this, the downloader won't work.

6. **Click "Install Now"** (the big button at the top)

7. **Wait** for it to finish installing (takes about 1-2 minutes)

8. **Click "Close"** when it says "Setup was successful"

✅ **Python is now installed!** You only need to do this once.

---

### Step 2: Download the Videos

1. **Open the folder** that contains all these files:
   - `DOWNLOAD_VIDEOS.bat`
   - `downloader.py`
   - `video_list.json`

2. **Double-click** on `DOWNLOAD_VIDEOS.bat`

3. A **black command window** will open and start downloading videos automatically

4. **That's it!** Just wait — it will download all 139 videos one by one.

---

## ❓ Frequently Asked Questions

### How long will it take?
It depends on your internet speed. Each video is around 100-500 MB. With a good connection, expect **3-6 hours** for all 139 videos.

### Can I stop in the middle and resume later?
**Yes!** You can close the window at any time. When you double-click `DOWNLOAD_VIDEOS.bat` again, it will **skip already-downloaded videos** and continue from where it stopped.

### Where are the downloaded videos saved?
In a folder called **`downloads`** inside the same folder where you ran the script.

### I see "yt-dlp is NOT installed" message. What do I do?
**Nothing!** The script will automatically install yt-dlp for you. Just wait a moment.

### The window shows red/error text. What went wrong?
Some videos might fail due to temporary internet issues. **Just run the script again** — it will automatically retry the failed ones and skip the successful ones.

### I see "Python is NOT installed" error after double-clicking
Go back to **Step 1** and install Python. Make sure you check the **"Add Python to PATH"** checkbox during installation.

### I installed Python but it still says "Python is NOT installed"
1. **Restart your computer** after installing Python
2. Try double-clicking `DOWNLOAD_VIDEOS.bat` again

### Can I download only a few videos instead of all 139?
The script downloads all remaining videos by default. If you want to stop after some videos, simply close the window. Progress is saved.

---

## 📂 Files in This Folder

| File | What it does |
|------|-------------|
| `DOWNLOAD_VIDEOS.bat` | **Double-click this to start downloading!** |
| `downloader.py` | The actual download program (don't edit this) |
| `video_list.json` | List of all 139 videos with YouTube links (don't edit this) |
| `video_urls.json` | Original list of video page URLs (backup, not needed) |
| `downloads/` | Folder where all downloaded videos are saved |

---

## 🆘 Need Help?

If something goes wrong and you can't figure it out:
1. Take a **screenshot** of the error message in the black window
2. Send the screenshot to the person who gave you this tool
