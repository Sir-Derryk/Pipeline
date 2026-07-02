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

echo Generating SWIG wrappers...

:: Run SWIG for Python
echo [Python] Running SWIG for core_modeler.i...
swig -python -doxygen -c++ -I"%~dp0..\engine\tests\assets\main\mock" -outdir "%~dp0..\engine\tests\assets\main\_swig\python\mock" -o "%~dp0..\engine\tests\assets\main\_swig\python\mock\core_modeler_wrap.cpp" "%~dp0..\engine\tests\assets\main\mock\core_modeler.i"
if %ERRORLEVEL% neq 0 (
    echo Error: Python SWIG generation failed.
    exit /b %ERRORLEVEL%
)

:: Run SWIG for C#
echo [C#] Running SWIG for core_modeler.i...
swig -csharp -c++ -I"%~dp0..\engine\tests\assets\main\mock" -outdir "%~dp0..\engine\tests\assets\main\_swig\csharp\mock" -o "%~dp0..\engine\tests\assets\main\_swig\csharp\mock\core_modeler_wrap.cxx" "%~dp0..\engine\tests\assets\main\mock\core_modeler.i"
if %ERRORLEVEL% neq 0 (
    echo Error: C# SWIG generation failed.
    exit /b %ERRORLEVEL%
)

:: Run SWIG for Java
echo [Java] Running SWIG for core_modeler.i...
swig -java -doxygen -c++ -I"%~dp0..\engine\tests\assets\main\mock" -outdir "%~dp0..\engine\tests\assets\main\_swig\java\mock" -o "%~dp0..\engine\tests\assets\main\_swig\java\mock\core_modeler_wrap.cxx" "%~dp0..\engine\tests\assets\main\mock\core_modeler.i"
if %ERRORLEVEL% neq 0 (
    echo Error: Java SWIG generation failed.
    exit /b %ERRORLEVEL%
)

echo SWIG wrappers successfully generated for Python, C# and Java!
endlocal
