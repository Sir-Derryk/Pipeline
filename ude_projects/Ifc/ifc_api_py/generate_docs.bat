@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

set "SCRIPT_DIR=%~dp0"

set "GLOBAL_CONFIG=..\..\ude_global_config.json"
set "SDK_CONFIG=..\ude_sdk_config.json"
set "DOC_CONFIG=ude_doc_config.json"

echo ============================================================
echo   Universal Doc Engine: UDE API Generation Launcher
echo ============================================================

:: Release mode: use isolated venv created by install.bat (no PYTHONPATH conflicts)
set "VENV_PYTHON=%SCRIPT_DIR%..\..\..\.venv\Scripts\python.exe"
if exist "%VENV_PYTHON%" (
    set "UDE_PYTHON=%VENV_PYTHON%"
    goto :run_ude
)

:: Dev mode: use system Python with PYTHONPATH pointing to engine source
python --version >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python is not installed or not found on system PATH.
    echo Please install Python 3.9 or higher and add it to PATH.
    exit /b 5
)

python -c "import pydantic, lxml, jinja2, markdown" >nul 2>&1
if %errorlevel% neq 0 (
    echo [INFO] Missing required python libraries. Attempting automatic installation...
    python -m pip install pydantic lxml jinja2 markdown
    if !errorlevel! neq 0 (
        echo [ERROR] Failed to install required python packages: pydantic, lxml, jinja2, markdown.
        exit /b 5
    )
)
set "PYTHONPATH=%SCRIPT_DIR%..\..\..\engine"
set "UDE_PYTHON=python"

:run_ude
"%UDE_PYTHON%" -m ude.cli --global-config "%GLOBAL_CONFIG%" --sdk-config "%SDK_CONFIG%" --doc-config "%DOC_CONFIG%" --format html
if %errorlevel% neq 0 (
    echo [ERROR] UDE Pipeline failed.
    exit /b 1
)

echo [OK]    Documentation generated successfully.
echo.
endlocal