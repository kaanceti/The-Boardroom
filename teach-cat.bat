@echo off
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
echo === Teaching the office cat ===
echo It reads your meetings, then practises for a few minutes. Leave this window open.
echo.
uv run --no-project cat/prepare.py || goto :fail
echo.
uv run --no-project --with numpy cat/tinycat.py train --steps 600 --every 100 --workers 2 || goto :fail
uv run --no-project --with numpy cat/tinycat.py export || goto :fail
echo.
echo What it says now:
uv run --no-project --with numpy cat/tinycat.py say -n 3
echo.
echo Done. Refresh The Boardroom to hear what it learned.
pause
exit /b 0
:fail
echo.
echo Something went wrong. Scroll up for the error.
pause
exit /b 1
