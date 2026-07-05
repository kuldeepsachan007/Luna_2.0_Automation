@echo off
REM ============================================================
REM  Run the Luna 2.0 Sleep BDD scenario.
REM  Activates the project virtualenv (myenv) so that the plain
REM  "pytest -m sleep" command uses the right interpreter/plugins.
REM  Allure results are written to allure-results automatically
REM  (see pytest.ini addopts).
REM
REM  Usage:  double-click this file, or from a terminal:  run_sleep.bat
REM ============================================================
cd /d "%~dp0"
call myenv\Scripts\activate.bat
pytest -m sleep -v
echo.
echo Done. Run allure_report.bat to view the Allure report.
pause
