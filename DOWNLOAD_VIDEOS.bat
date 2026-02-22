@echo off
title GuruMantra Video Downloader
echo.
echo ============================================================
echo    GuruMantra Video Downloader - One-Click Launcher
echo ============================================================
echo.

REM Change to the directory where this .bat file is located
cd /d "%~dp0"

REM Try running with "python" first
python --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found! Starting download...
    echo.
    python downloader.py
    goto :end
)

REM Try running with "py" (Python Launcher for Windows)
py --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found! Starting download...
    echo.
    py downloader.py
    goto :end
)

REM Try running with "python3"
python3 --version >nul 2>&1
if %errorlevel% equ 0 (
    echo [OK] Python found! Starting download...
    echo.
    python3 downloader.py
    goto :end
)

REM Python not found
echo.
echo ============================================================
echo    ERROR: Python is NOT installed on this computer!
echo ============================================================
echo.
echo    Please follow these steps to install Python:
echo.
echo    1. Open your web browser
echo    2. Go to: https://www.python.org/downloads/
echo    3. Click the big yellow "Download Python" button
echo    4. Run the downloaded file
echo    5. IMPORTANT: Check the box that says "Add Python to PATH"
echo    6. Click "Install Now"
echo    7. After installation, come back and double-click
echo       this file (DOWNLOAD_VIDEOS.bat) again
echo.
echo ============================================================
echo.

:end
pause
