@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion

echo ============================================================
echo   UDE: Building all Mock SDK Documentation
echo ============================================================

set "PROJECTS=mock_api_cpp mock_api_cs mock_api_java mock_api_py"

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
echo   [SUCCESS] All Mock projects processing finished.
echo ============================================================
