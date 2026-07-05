@echo off
REM ============================================================
REM  Parallel multi-device Luna test runner.
REM  Default (no args): runs the per-device markers from
REM  parallel\devices.json  ->  heart_rate on device 1,
REM  stress on device 2, at the same time.
REM
REM  Examples:
REM     run_parallel.bat
REM     run_parallel.bat heart_rate stress
REM     run_parallel.bat heart_rate@70f31eb6b9fc stress@TWL77DU8U4TKIBYT
REM     run_parallel.bat --report
REM ============================================================
cd /d "%~dp0\.."
call myenv\Scripts\activate.bat
python parallel\run_parallel.py %*
echo.
echo Done. Run parallel\report.bat to view the combined Allure report.
pause
