@echo off
REM ============================================================
REM  Open the Allure report for the latest run.
REM  Starts a local web server and opens the report in the browser.
REM  Press Ctrl+C in this window to stop the server.
REM
REM  Usage:  double-click this file, or from a terminal:  allure_report.bat
REM ============================================================
cd /d "%~dp0"
call allure serve allure-results
