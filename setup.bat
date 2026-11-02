@echo off
setlocal
cd /d "%~dp0"
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
echo === The Boardroom setup ===
echo.
where claude >nul 2>&1 || (
  echo Installing Claude Code...
  powershell -NoProfile -ExecutionPolicy ByPass -Command "irm https://claude.ai/install.ps1 | iex"
)
where uv >nul 2>&1 || (
  echo Installing uv ^(runs Python for the app^)...
  powershell -NoProfile -ExecutionPolicy ByPass -Command "irm https://astral.sh/uv/install.ps1 | iex"
)
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
where claude >nul 2>&1 || goto :noclaude
echo.
claude auth status >nul 2>&1
if errorlevel 1 (
  echo Sign in with your Claude Pro account in the browser window that opens.
  claude auth login
)
echo.
claude auth status --text
echo.
echo Setup complete. Double-click start.bat to open The Boardroom.
pause
exit /b 0
:noclaude
echo.
echo Claude Code did not install. Scroll up for the error, or install it from https://code.claude.com
pause
exit /b 1
