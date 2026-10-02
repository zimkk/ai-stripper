@echo off
title AI-STRIPPER • Privacy Shield
cd /d "%~dp0"

echo ========================================================
echo   AI-STRIPPER: Initializing Privacy Engine...
echo ========================================================
echo.

:: 1. Check if Python is installed
where python >nul 2>nul
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python is not installed or not in your PATH!
    echo Please install Python from https://www.python.org/downloads/
    echo (Make sure to check "Add Python to PATH" during installation)
    echo.
    pause
    exit /b 1
)

:: 2. Install / verify dependencies
echo [*] Checking dependencies...
python -m pip install -q -r requirements.txt

:: 3. Launch the Interactive Terminal App
echo [*] Launching AI-STRIPPER...
echo.
python stripper.py

:: If it exits with an error or user closes
if %ERRORLEVEL% neq 0 (
    echo.
    echo [!] Application exited with an error.
    pause
)
