@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo AI COMMERCE - SINGLE CLICK LOCAL DOCKER (CORE / LOW MEMORY)
echo ============================================================
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-local-docker.ps1"
if errorlevel 1 pause
