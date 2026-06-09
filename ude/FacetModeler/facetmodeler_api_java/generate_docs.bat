@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"
set "PYTHON_ROOT=%SCRIPT_DIR%..\..\..\engine"
set "CONFIG=%SCRIPT_DIR%ude_config.json"

echo ============================================================
echo   Universal Doc Engine: UDE API Generation Launcher
echo ============================================================

:: 1. Verify Python availability
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found on system PATH.
    echo Please install Python 3.9 or higher and add it to PATH.
    exit /b 5
)

:: 2. Pre-flight auto-install dependencies if missing
python -c "import pydantic, lxml, jinja2" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Missing required python libraries. Attempting automatic installation...
    python -m pip install pydantic lxml jinja2
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install required python packages (pydantic, lxml, jinja2).
        exit /b 5
    )
)

:: 3. Run UDE Orchestrator
set "PYTHONPATH=%PYTHON_ROOT%"
python -m oda_ude.orchestrator "%CONFIG%"

if %errorlevel% neq 0 (
    echo [ERROR] UDE Pipeline failed.
    exit /b 1
)

echo [OK]    Documentation generated successfully.
echo.
endlocal
