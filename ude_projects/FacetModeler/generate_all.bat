@echo off
chcp 65001 >nul
setlocal enabledelayedexpansion
pushd "%~dp0"

for %%i in ("%~dp0.") do set "SDK_NAME=%%~nxi"

echo ============================================================
echo   UDE: Building all %SDK_NAME% Documentation
echo ============================================================

set "FOUND=0"
for /d %%p in (*) do (
    if exist "%%p\generate_docs.bat" (
        set "FOUND=1"
        echo.
        echo [BUILD] Processing project: %%p
        pushd "%%p"
        call generate_docs.bat
        if !errorlevel! neq 0 (
            echo [ERROR] Build failed for project: %%p
            popd
            popd
            exit /b 1
        )
        popd
    )
)

if "!FOUND!"=="0" (
    echo [WARN] No projects with generate_docs.bat found.
)

echo.
echo ============================================================
echo   [SUCCESS] All %SDK_NAME% projects processing finished.
echo ============================================================
popd
