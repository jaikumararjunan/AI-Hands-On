@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo AI COMMERCE - END TO END APPLICATION TEST
echo ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\test-application.ps1"
set RC=%ERRORLEVEL%
if not "%RC%"=="0" (
  echo.
  echo Application test FAILED. Review the failed row(s) above.
  pause
  exit /b %RC%
)
echo.
echo Application test PASSED.
pause
exit /b 0
