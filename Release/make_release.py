#!/usr/bin/env python3
"""UDE release packaging utility.

Lives in Release/. Reads ude_release_manifest.json from the parent repo root,
clears and rebuilds only Release/ude/ on every run.
"""

import json
import os
import shutil
from pathlib import Path

RELEASE_DIR = Path(__file__).resolve().parent
REPO_ROOT = RELEASE_DIR.parent
MANIFEST_PATH = RELEASE_DIR / "ude_release_manifest.json"
RELEASE_UDE_DIR = RELEASE_DIR / "ude"
UDE_PROJECTS_DIR = REPO_ROOT / "ude_projects"


_INSTALL_BAT = """\
@echo off
setlocal enabledelayedexpansion

:: %~dp0 always resolves to the directory of this script, regardless of CWD
set "ROOT=%~dp0"
if "%ROOT:~-1%"=="\\" set "ROOT=%ROOT:~0,-1%"

pushd "%ROOT%"

echo ===================================================
echo  UDE Environment Setup
echo  Base directory: %ROOT%
echo ===================================================

:: --- Python Check ---
echo Checking Python...
where python >nul 2>&1
if %errorlevel% neq 0 (
    echo [ERROR] Python was not found on your system PATH.
    echo Please install Python 3.11 or higher.
    popd & pause & exit /b 1
)
for /f "tokens=2 delims= " %%v in ('python --version 2^>^&1') do set PYVER=%%v
for /f "tokens=1,2 delims=." %%a in ("%PYVER%") do (set PYMAJ=%%a & set PYMIN=%%b)
if %PYMAJ% LSS 3 (
    echo [ERROR] Python %PYVER% is too old. Version 3.11 or higher is required.
    popd & pause & exit /b 1
)
if %PYMAJ% EQU 3 if %PYMIN% LSS 11 (
    echo [ERROR] Python %PYVER% is too old. Version 3.11 or higher is required.
    popd & pause & exit /b 1
)
echo [OK] Python %PYVER% found.

:: --- Doxygen Check ---
echo Checking Doxygen...
where doxygen >nul 2>&1
if %errorlevel% neq 0 (
    echo [WARNING] Doxygen was not found on PATH.
    echo Documentation generation will not be available.
    echo Place the Doxygen binary in: %ROOT%\\tools\\doxygen\\ and add it to PATH.
) else (
    echo [OK] Doxygen found.
)

:: --- Remove stale virtual environment ---
:: CRITICAL: a copied .venv embeds absolute paths from the source machine and
::           will not function correctly at any other location.
echo.
echo Cleaning up any stale virtual environment...
if exist "%ROOT%\\.venv" (
    echo [INFO] Removing stale .venv...
    rmdir /s /q "%ROOT%\\.venv"
    if exist "%ROOT%\\.venv" (
        echo [ERROR] Could not remove %ROOT%\\.venv. Close all processes using it.
        popd & pause & exit /b 1
    )
    echo [OK] Stale .venv removed.
) else (
    echo [OK] No stale .venv found.
)

:: --- Create fresh virtual environment ---
echo.
echo Creating fresh virtual environment at: %ROOT%\\.venv
python -m venv "%ROOT%\\.venv"
if %errorlevel% neq 0 (
    echo [ERROR] Failed to create virtual environment.
    popd & pause & exit /b 1
)
echo [OK] Virtual environment created.

:: --- Install UDE engine ---
echo.
echo Installing UDE engine...
call "%ROOT%\\.venv\\Scripts\\activate.bat"
python -m pip install --upgrade pip --quiet
pip install "%ROOT%\\engine"
if %errorlevel% neq 0 (
    echo [ERROR] UDE installation failed.
    echo Make sure engine\\README.md is present in the engine\\ directory.
    popd & pause & exit /b 1
)
echo [OK] UDE installed successfully.

:: --- Verify installation ---
echo.
echo Verifying installation...
"%ROOT%\\.venv\\Scripts\\ude.exe" --help
if %errorlevel% neq 0 (
    echo [WARNING] 'ude --help' exited with an error. Verify the installation manually.
)

popd
echo.
echo ===================================================
echo  Installation complete.
echo  To activate the environment run:
echo    call "%ROOT%\\.venv\\Scripts\\activate.bat"
echo ===================================================
pause
"""

_UNINSTALL_BAT = """\
@echo off
echo ===================================================
echo UDE Uninstaller: Cleaning up isolated environment...
echo ===================================================

if not exist .venv goto :no_venv

echo Removing local virtual environment (.venv)...
rmdir /s /q .venv
if %errorlevel% neq 0 goto :remove_failed
echo [OK] Environment successfully de-initialized.
goto :end

:remove_failed
echo [ERROR] Could not remove .venv. Some files may be in use.
echo         Close any active terminals using this environment and try again.
goto :end

:no_venv
echo [SKIP] No .venv directory found in this folder. Nothing to remove.

:end
echo.
pause
"""

_GITIGNORE = """\
.venv/
__pycache__/
.pytest_cache/
*.pyc
"""

_RUN_ALL_SDKS_BAT = """\
@echo off
pushd "%~dp0"
echo ===================================================
echo UDE Global Runner: Activating environment...
echo ===================================================

set "VENV_ACTIVATE=%~dp0..\\.venv\\Scripts\\activate.bat"
if not exist "%VENV_ACTIVATE%" (
    echo [ERROR] Virtual environment not found at:
    echo         %VENV_ACTIVATE%
    echo         Run install.bat from the UDE root first.
    popd
    pause
    exit /b 1
)
call "%VENV_ACTIVATE%"

echo ===================================================
echo UDE Global Runner: Processing all active SDK families...
echo ===================================================
for /d %%d in (*) do (
    if exist "%%d\\generate_all.bat" (
        echo Entering SDK family folder: %%d
        call "%%d\\generate_all.bat"
    )
)
popd
pause
"""


def _resolve_project_info(project_name: str) -> tuple[str, str, Path] | None:
    """Map 'SdkName API Lang' to (sdk_key, lang_api_folder, disk_path)."""
    parts = project_name.split(" API ")
    if len(parts) != 2:
        return None
    sdk, lang = parts
    sdk_key = sdk.lower()
    lang_api_folder = f"{sdk_key}_api_{lang.lower()}"
    candidate = UDE_PROJECTS_DIR / sdk_key / lang_api_folder
    return (sdk_key, lang_api_folder, candidate) if candidate.exists() else None


def _write_install_bat() -> None:
    bat_path = RELEASE_UDE_DIR / "install.bat"
    bat_path.write_text(_INSTALL_BAT, encoding="utf-8")
    print(f"Generated:    Release/ude/install.bat")


def _write_uninstall_bat() -> None:
    bat_path = RELEASE_UDE_DIR / "uninstall.bat"
    bat_path.write_text(_UNINSTALL_BAT, encoding="utf-8")
    print(f"Generated:    Release/ude/uninstall.bat")


def _write_gitignore() -> None:
    gitignore_path = RELEASE_UDE_DIR / ".gitignore"
    gitignore_path.write_text(_GITIGNORE, encoding="utf-8")
    print(f"Generated:    Release/ude/.gitignore")


def _write_run_all_sdks_bat() -> None:
    bat_path = RELEASE_UDE_DIR / "ude_projects" / "run_all_sdks.bat"
    bat_path.write_text(_RUN_ALL_SDKS_BAT, encoding="utf-8")
    print(f"Generated:    Release/ude/ude_projects/run_all_sdks.bat")


def _copy_config_files(sdk_keys: list[str]) -> None:
    src_global = UDE_PROJECTS_DIR / "ude_global_config.json"
    if not src_global.exists():
        print(f"[WARNING] {src_global.name} not found. Skipping config copy.")
        return

    global_cfg = json.loads(src_global.read_text(encoding="utf-8"))
    global_cfg["output_base_dir"] = "../../../ude_output"

    dest_projects_dir = RELEASE_UDE_DIR / "ude_projects"
    dest_global = dest_projects_dir / "ude_global_config.json"
    dest_global.write_text(json.dumps(global_cfg, indent=4), encoding="utf-8")
    print(f"Patched:      ude_global_config.json -> Release/ude/ude_projects/ude_global_config.json")

    for sdk_key in sdk_keys:
        src_sdk = UDE_PROJECTS_DIR / sdk_key / "ude_sdk_config.json"
        if not src_sdk.exists():
            print(f"[WARNING] ude_sdk_config.json not found for '{sdk_key}'. Skipping.")
            continue
        dest_sdk_dir = dest_projects_dir / sdk_key
        dest_sdk_dir.mkdir(exist_ok=True)
        shutil.copy2(src_sdk, dest_sdk_dir / "ude_sdk_config.json")
        print(f"Copied:       ude_projects/{sdk_key}/ude_sdk_config.json -> Release/ude/ude_projects/{sdk_key}/ude_sdk_config.json")


def main() -> None:
    manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
    core_files: list[str] = manifest["core_files"]
    projects: list[str] = manifest.get("projects", [])

    # Print manifest to console
    print("=== UDE Minimum Runtime Manifest ===")
    for path in core_files:
        print(f"  {path}")
    print(f"\n{len(core_files)} core files total.\n")

    # Clear and reinitialise only Release/ude/
    if RELEASE_UDE_DIR.exists():
        shutil.rmtree(RELEASE_UDE_DIR)
    RELEASE_UDE_DIR.mkdir()
    print(f"Cleared:      Release/ude/")

    # Generate environment batch files and gitignore
    _write_install_bat()
    _write_uninstall_bat()
    _write_gitignore()

    # Copy core files preserving relative hierarchy
    for rel_path in core_files:
        src = REPO_ROOT / rel_path
        dst = RELEASE_UDE_DIR / rel_path
        os.makedirs(dst.parent, exist_ok=True)
        shutil.copy2(src, dst)
    print(f"Copied:       {len(core_files)} core files -> Release/ude/")

    # Prepare ude_projects/ and generate global runner
    release_projects_dir = RELEASE_UDE_DIR / "ude_projects"
    release_projects_dir.mkdir(exist_ok=True)
    _write_run_all_sdks_bat()

    sdk_keys: list[str] = []

    # Copy project trees under sdk/lang_api hierarchy
    for project_name in projects:
        info = _resolve_project_info(project_name)
        if info is None:
            print(f"[WARNING] Project '{project_name}' not found on disk. Skipping.")
            continue
        sdk_key, lang_api_folder, project_path = info
        if sdk_key not in sdk_keys:
            sdk_keys.append(sdk_key)

        # Initialise SDK family directory
        release_sdk_dir = release_projects_dir / sdk_key
        release_sdk_dir.mkdir(exist_ok=True)

        # Copy intermediate SDK-level generate_all.bat if present
        src_generate_all = UDE_PROJECTS_DIR / sdk_key / "generate_all.bat"
        if src_generate_all.exists():
            shutil.copy2(src_generate_all, release_sdk_dir / "generate_all.bat")
            print(f"Copied:       ude_projects/{sdk_key}/generate_all.bat -> Release/ude/ude_projects/{sdk_key}/generate_all.bat")

        # Recursively copy the specific project folder (includes generate_docs.bat)
        dest = release_sdk_dir / lang_api_folder
        shutil.copytree(project_path, dest)
        print(f"Copied:       project '{project_name}' -> Release/ude/ude_projects/{sdk_key}/{lang_api_folder}/")

    # Patch release copies of project config files:
    # dev paths use ../../../  (3 levels up to repo root)
    # release paths need extra levels because release root sits deeper in the filesystem
    for doc_config in release_projects_dir.rglob("ude_doc_config.json"):
        text = doc_config.read_text(encoding="utf-8")
        if "../../../main/" in text:
            doc_config.write_text(text.replace("../../../main/", "../../../../../main/"), encoding="utf-8")
            print(f"Patched:      src_dir in {doc_config.relative_to(RELEASE_UDE_DIR)}")

    for sidebar in release_projects_dir.rglob("sidebar.toml"):
        text = sidebar.read_text(encoding="utf-8")
        if 'source_file = "../../../' in text:
            text = text.replace('source_file = "../../../', 'source_file = "../../../../')
            sidebar.write_text(text, encoding="utf-8")
            print(f"Patched:      source_file paths in {sidebar.relative_to(RELEASE_UDE_DIR)}")

    for gen_docs in release_projects_dir.rglob("generate_docs.bat"):
        text = gen_docs.read_text(encoding="utf-8")
        if 'python -m ude.cli' in text and 'UDE_PYTHON' not in text:
            text = text.replace(
                'python -m ude.cli',
                'set "UDE_PYTHON=..\\..\\..\\.venv\\Scripts\\python.exe"\n'
                'if not exist "%UDE_PYTHON%" set "UDE_PYTHON=python"\n'
                '\n'
                '%UDE_PYTHON% -m ude.cli',
            )
            gen_docs.write_text(text, encoding="utf-8")
            print(f"Patched:      venv fallback in {gen_docs.relative_to(RELEASE_UDE_DIR)}")

    # Copy and patch environment configuration JSONs
    _copy_config_files(sdk_keys)

    print("\nRelease build complete.")


if __name__ == "__main__":
    main()
