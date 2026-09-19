@echo off
cd /d "%~dp0"
set "PYTHONUTF8=1"
set "PATH=%~dp0.venv311\Scripts;%PATH%"
"%~dp0.venv311\Scripts\python.exe" "%~dp0start_webui.py"
if errorlevel 1 pause
