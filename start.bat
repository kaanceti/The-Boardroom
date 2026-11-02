@echo off
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
start "The Boardroom" /min cmd /k "uv run --no-project boardroom.py"
timeout /t 4 /nobreak >nul
start "" http://localhost:8765
