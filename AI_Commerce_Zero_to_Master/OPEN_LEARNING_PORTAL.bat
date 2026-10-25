@echo off
setlocal enabledelayedexpansion
cd /d "%~dp0"
set LEARNING_PORT=9100
if exist ".env.local" (
  for /f "usebackq tokens=1,* delims==" %%A in (".env.local") do (
    if /I "%%A"=="LEARNING_PORT" set LEARNING_PORT=%%B
  )
)
echo Opening Learning Portal at http://localhost:%LEARNING_PORT%
start "" "http://localhost:%LEARNING_PORT%"
