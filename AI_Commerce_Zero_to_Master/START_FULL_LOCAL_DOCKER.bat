@echo off
setlocal
cd /d "%~dp0"
echo ============================================================
echo AI COMMERCE - SINGLE CLICK FULL LOCAL DOCKER
echo Adds Grafana + Prometheus + OpenTelemetry + MLflow
echo ============================================================
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\start-local-docker.ps1" -Full
if errorlevel 1 pause
