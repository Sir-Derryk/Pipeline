@echo off
:: Universal Documentation Engine (UDE) - Git History Compression Script (Orphan Branch Method)
:: This script collapses the history of all three submodules and the parent repository into 1 commit.
:: WARNING: Make sure you have temporarily disabled Rulesets / Branch Protections on GitHub for all 4 repositories!

set "ROOT_DIR=%~dp0"
:: Remove trailing slash if present
if "%ROOT_DIR:~-1%"=="\" set "ROOT_DIR=%ROOT_DIR:~0,-1%"

echo ======================================================================
echo  [UDE] STARTING GIT HISTORY COMPRESSION (ORPHAN BRANCH METHOD)
echo ======================================================================
echo ROOT_DIR is set to: %ROOT_DIR%
echo.
echo WARNING: This script will completely rewrite the git history of 
echo the parent repository and all three submodules into exactly 1 commit.
echo.
pause

:: 1. Compressing submodule 'engine' (default branch: master)
echo.
echo === [1/4] Compressing submodule 'engine' (master) ===
cd "%ROOT_DIR%\engine" || goto :error
git checkout --orphan temp_engine || goto :error
git add -A || goto :error
git commit -m "Initial commit (Universal Documentation Engine Core)" || goto :error
git branch -D master || goto :error
git branch -m master || goto :error
echo Pushing engine 'master' to remote (force push)...
git push -f origin master || goto :error
echo engine compressed successfully!

:: 2. Compressing submodule 'user-docs' (default branch: main)
echo.
echo === [2/4] Compressing submodule 'user-docs' (main) ===
cd "%ROOT_DIR%\user-docs" || goto :error
git checkout --orphan temp_user_docs || goto :error
git add -A || goto :error
git commit -m "Initial commit (User and Admin Guides)" || goto :error
git branch -D main || goto :error
git branch -m main || goto :error
echo Pushing user-docs 'main' to remote (force push)...
git push -f origin main || goto :error
echo user-docs compressed successfully!

:: 3. Compressing submodule 'design-docs' (default branch: main)
echo.
echo === [3/4] Compressing submodule 'design-docs' (main) ===
cd "%ROOT_DIR%\design-docs" || goto :error
git checkout --orphan temp_design_docs || goto :error
git add -A || goto :error
git commit -m "Initial commit (Design and SRS Documentation)" || goto :error
git branch -D main || goto :error
git branch -m main || goto :error
echo Pushing design-docs 'main' to remote (force push)...
git push -f origin main || goto :error
echo design-docs compressed successfully!

:: 4. Compressing parent repository 'Pipeline' (default branch: master)
echo.
echo === [4/4] Updating submodule pointers and compressing parent repository 'Pipeline' (master) ===
cd "%ROOT_DIR%" || goto :error
echo Staging updated submodule pointers...
git add engine user-docs design-docs || goto :error
echo Creating orphan branch for parent repository...
git checkout --orphan temp_pipeline || goto :error
:: Note: We do NOT run "git add -A" here to prevent staging large untracked files like Pipeline.rar (already deleted, but kept for robustness).
:: Since the index is already populated with tracked files, we commit the current index containing
:: the updated submodule pointers and all previously tracked project files.
git commit -m "Initial commit (Universal Documentation Portal)" || goto :error
git branch -D master || goto :error
git branch -m master || goto :error
echo Pushing parent 'master' to remote (force push)...
git push -f origin master || goto :error
echo Parent repository compressed successfully!

echo.
echo ======================================================================
echo  SUCCESS: All 4 repositories have been successfully compressed to 1 commit!
echo  Don't forget to re-enable your Rulesets/Branch Protections on GitHub!
echo ======================================================================
pause
exit /b 0

:error
echo.
echo ======================================================================
echo  ERROR: An error occurred during the compression process.
echo  Execution halted to prevent data or repository corruption.
echo ======================================================================
pause
exit /b 1
