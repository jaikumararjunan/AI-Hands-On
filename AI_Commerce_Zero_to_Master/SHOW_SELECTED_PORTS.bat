@echo off
cd /d "%~dp0"
if not exist .env.local (
  echo .env.local does not exist yet. Start Docker once first.
  pause
  exit /b 1
)
echo ============================================================
echo AI COMMERCE - CURRENT SELECTED HOST PORTS
 echo ============================================================
type .env.local
pause
