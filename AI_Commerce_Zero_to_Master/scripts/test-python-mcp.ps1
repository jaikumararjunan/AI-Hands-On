$ErrorActionPreference = "Stop"
Set-Location "$PSScriptRoot\..\ai-python"
.\.venv\Scripts\Activate.ps1
python -m app.mcp.mcp_client_demo
