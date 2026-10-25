param(
    [int]$Count = 3,
    [string]$JavaUrl = "http://127.0.0.1:8080",
    [string]$PythonUrl = "http://127.0.0.1:8000"
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
python "$Root\mock-data\exercise_running_services.py" `
  --count $Count `
  --java-url $JavaUrl `
  --python-url $PythonUrl
