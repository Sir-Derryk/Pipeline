@echo off
chcp 65001 >nul
setlocal
pushd "%~dp0"

set "GLOBAL_CONFIG=..\..\ude_global_config.json"
set "SDK_CONFIG=..\ude_sdk_config.json"
set "DOC_CONFIG=ude_doc_config.json"

echo ============================================================
echo   Universal Doc Engine: UDE API Generation Launcher
echo ============================================================

:: --- Resolve Python interpreter: prefer .venv, fall back to PYTHONPATH injection ---
set "UDE_PYTHON=%~dp0..\..\..\.venv\Scripts\python.exe"
if not exist "%UDE_PYTHON%" (
    set "PYTHONPATH=%~dp0..\..\..\engine;%PYTHONPATH%"
    set "UDE_PYTHON=python"
    echo [INFO] No .venv found. Injecting engine path into PYTHONPATH.
) else (
    echo [INFO] Using .venv: %UDE_PYTHON%
)

"%UDE_PYTHON%" -m ude.cli --global-config "%GLOBAL_CONFIG%" --sdk-config "%SDK_CONFIG%" --doc-config "%DOC_CONFIG%" --format html
if %errorlevel% neq 0 (
    echo [ERROR] UDE Pipeline failed.
    popd
	pause
    exit /b 1
)

echo [OK]    Documentation generated successfully.
popd
pause
endlocal
