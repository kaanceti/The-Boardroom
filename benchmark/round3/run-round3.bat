@echo off
cd /d "%~dp0..\.."
set "PATH=%USERPROFILE%\.local\bin;%PATH%"
echo === Blind test, round 3: today's board against Claude Opus on its own ===
echo 15 new questions. Each one gets a full board meeting and one answer from Opus on its own.
echo It saves after every question, so you can close this window at any time and double-click again to carry on.
echo If your Claude plan reaches its usage limit, it stops by itself. Run it again once the limit resets.
echo Keep the laptop awake while it runs.
echo.
uv run --no-project benchmark\round3\run.py
if errorlevel 2 goto :later
if errorlevel 1 goto :fail
echo.
echo Every question is answered. Now a separate Opus judges each pair twice (30 calls).
uv run --no-project benchmark\round3\judge.py
if errorlevel 2 goto :later
if errorlevel 1 goto :fail
echo.
echo Round 3 is finished. Tell Claude, and it will write up the results.
pause
exit /b 0
:later
echo.
echo Stopped before the end. Double-click this file again later to carry on where it stopped.
pause
exit /b 0
:fail
echo.
echo Something went wrong. Scroll up for the error.
pause
exit /b 1
