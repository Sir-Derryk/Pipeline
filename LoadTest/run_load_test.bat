@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
cd /d "%SCRIPT_DIR%.."

echo ============================================================
echo   Starting ODA SDK Python HTML Doc Load Testing...
echo ============================================================

set "PYTHON_EXE=engine\.venv\Scripts\python.exe"
set "PYTHONPATH=engine"

if not exist "%PYTHON_EXE%" (
    echo [ERROR] Python Virtual Environment not found at: %PYTHON_EXE%
    echo Please make sure the virtual environment is initialized in engine/
    exit /b 1
)

"%PYTHON_EXE%" LoadTest\run_load_test.py

echo.
echo ============================================================
echo   Load Testing Finished. Check LoadTest\report.md for results.
echo ============================================================
endlocal
