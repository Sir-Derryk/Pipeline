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

python -m ude.cli --global-config "%GLOBAL_CONFIG%" --sdk-config "%SDK_CONFIG%" --doc-config "%DOC_CONFIG%" --format html
if %errorlevel% neq 0 (
    echo [ERROR] UDE Pipeline failed.
    popd
    exit /b 1
)

echo [OK]    Documentation generated successfully.
popd
endlocal
