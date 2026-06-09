@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo   UDE: Building all Map Documentation
echo ============================================================

set "PROJECTS=map_api_cpp map_api_cs"

for %%p in (%PROJECTS%) do (
    echo.
    echo [BUILD] Processing project: %%p
    pushd %%p
    if exist generate_docs.bat (
        call generate_docs.bat
    ) else (
        echo [WARN] generate_docs.bat not found in %%p
    )
    if !errorlevel! neq 0 (
        echo [ERROR] Build failed for project: %%p
        popd
        exit /b 1
    )
    popd
)

echo.
echo ============================================================
echo   [SUCCESS] All Map projects processing finished.
echo ============================================================
