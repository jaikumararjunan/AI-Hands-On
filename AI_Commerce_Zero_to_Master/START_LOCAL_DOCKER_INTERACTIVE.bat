@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo AI COMMERCE - INTERACTIVE LOCAL DOCKER
 echo Select or change every host port before deployment
 echo ============================================================
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-local-docker.ps1" -PortMode Interactive
if errorlevel 1 (
  echo.
  echo Startup failed. Review diagnostics above.
)
pause
