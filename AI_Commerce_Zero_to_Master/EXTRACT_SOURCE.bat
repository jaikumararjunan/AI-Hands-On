@echo off
setlocal
cd /d "%~dp0"
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0EXTRACT_SOURCE.ps1"
if errorlevel 1 (
  echo.
  echo Extraction failed. Review the error above.
  pause
  exit /b 1
)
echo.
echo Source extraction completed.
pause
