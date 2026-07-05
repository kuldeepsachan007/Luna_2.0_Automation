@echo off
REM ============================================================
REM  Build + open a combined Allure report for the last parallel
REM  run (merges every device's results into one report).
REM ============================================================
cd /d "%~dp0\.."
call myenv\Scripts\activate.bat
python parallel\report.py
