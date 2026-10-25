$ErrorActionPreference = "Stop"
Push-Location "$PSScriptRoot\..\data-platform\pipelines"
try {
  python .\run_pipeline.py
} finally {
  Pop-Location
}
