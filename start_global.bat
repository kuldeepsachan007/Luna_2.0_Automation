@echo off
title Luna Global Launcher
REM Double-click: backend + tunnel start karke dashboard browser me khol dega.
REM Phone connected hona chahiye. Is window ko band mat karo (tunnel yahin chalta hai).
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0start_global.ps1"
echo.
echo (Window band karne ke liye koi bhi key dabao)
pause >nul
