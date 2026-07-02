@echo off
:: UDE - PowerShell Bypass Execution Wrapper
:: IMPORTANT: Before running with -PushToRemote, you MUST temporarily deactivate Rulesets / Branch Protection Rules on GitHub!
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0compress_history.ps1" %*
