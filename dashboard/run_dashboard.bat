@echo off
REM ============================================================
REM  Luna Automation Dashboard
REM  Starts the Flask backend + web UI on http://127.0.0.1:5000
REM  From there you can run Sleep / Heart Rate / Stress suites
REM  (full suite or a single test) on their mapped devices, in
REM  parallel, with live logs + a results summary.
REM ============================================================
cd /d "%~dp0\.."
call myenv\Scripts\activate.bat
echo.
echo   Dashboard starting -> http://127.0.0.1:5000
echo   (Ctrl+C to stop)
echo.
python dashboard\app.py
pause
