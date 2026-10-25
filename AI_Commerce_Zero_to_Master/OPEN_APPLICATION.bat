@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
set APP_PORT=9200
if exist ".env.local" (
  for /f "usebackq tokens=1,* delims==" %%A in (".env.local") do (
    if /I "%%A"=="APP_PORT" set APP_PORT=%%B
  )
)
echo Opening AI Commerce Application at http://localhost:%APP_PORT%
start "" "http://localhost:%APP_PORT%"
