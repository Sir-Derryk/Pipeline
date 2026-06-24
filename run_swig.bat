@echo off
setlocal
:: Add SWIG to PATH
set "PATH=C:\Users\derry\.gemini\swigwin-4.0.2\swigwin-4.0.2;%PATH%"

:: Verify SWIG
echo Checking SWIG version...
swig -version
if %ERRORLEVEL% neq 0 (
    echo Error: SWIG is not found at C:\Users\derry\.gemini\swigwin-4.0.2\swigwin-4.0.2 or failed to execute.
    exit /b 1
)

:: Run SWIG with -doxygen for the mock SDK
echo Running SWIG for core_modeler.i...
swig -python -doxygen -c++ -Iengine\tests\assets\main\mock -outdir "engine\tests\assets\main\_swig\python\mock" -o "engine\tests\assets\main\_swig\python\mock\core_modeler_wrap.cpp" "engine\tests\assets\main\mock\core_modeler.i"

if %ERRORLEVEL% EQU 0 (
    echo SWIG wrappers successfully generated!
) else (
    echo Error: SWIG generation failed with exit code %ERRORLEVEL%.
)
endlocal
