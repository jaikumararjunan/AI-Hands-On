$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\ai-python"
if (-not (Test-Path ".venv")) { python -m venv .venv }
.\.venv\Scripts\Activate.ps1
python -m pip install -r requirements.txt
python -m app.mcp.commerce_mcp_server
