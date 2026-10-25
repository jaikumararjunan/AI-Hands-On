$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\ai-python"
if (-not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
