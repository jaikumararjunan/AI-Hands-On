$ErrorActionPreference = "Stop"

$Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path
Write-Host "AI Commerce Control Center validation"
Write-Host "Root: $Root"

Write-Host "`n[1/8] Python syntax"
Push-Location (Join-Path $Root "ai-python")
python -m compileall -q .
if ($LASTEXITCODE -ne 0) { throw "Python syntax validation failed" }

Write-Host "`n[2/8] Python tests"
python -m pytest -q
if ($LASTEXITCODE -ne 0) { throw "Python tests failed" }
Pop-Location

Write-Host "`n[3/8] Mock-data generator"
Push-Location (Join-Path $Root "mock-data")
python .\generate_mock_data.py --profile tiny --scenario normal --seed 42 --as-of 2026-10-25T00:00:00+00:00 --reset
if ($LASTEXITCODE -ne 0) { throw "Mock-data generation failed" }
python .\validate_mock_data.py
if ($LASTEXITCODE -ne 0) { throw "Mock-data validation failed" }
Pop-Location

Write-Host "`n[4/8] Java tests"
Push-Location (Join-Path $Root "backend-java\commerce-core")
mvn test
if ($LASTEXITCODE -ne 0) { throw "Java tests failed" }
Pop-Location

Write-Host "`n[5/8] Docker Compose data stack"
Push-Location (Join-Path $Root "infra")
docker compose -f docker-compose-data.yml config | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Data-stack Compose validation failed" }
docker compose -f docker-compose-observability.yml config | Out-Null
if ($LASTEXITCODE -ne 0) { throw "Observability Compose validation failed" }
Pop-Location

Write-Host "`n[6/8] Vector math smoke demo"
Push-Location (Join-Path $Root "ai-python")
$env:VECTOR_BACKEND = "memory"
$env:EMBEDDING_PROVIDER = "hash"
python .\vector_from_scratch_demo.py
if ($LASTEXITCODE -ne 0) { throw "Vector smoke demo failed" }
Pop-Location

Write-Host "`n[7/8] Historical data pipeline"
Push-Location (Join-Path $Root "data-platform\pipelines")
python .\run_pipeline.py
if ($LASTEXITCODE -ne 0) { throw "Data pipeline validation failed" }
Pop-Location

Write-Host "`n[8/8] Learning portal files"
$LearningSite = Join-Path $Root "learning-site"
foreach ($File in @("index.html", "styles.css", "app.js")) {
    if (-not (Test-Path (Join-Path $LearningSite $File))) { throw "Missing learning-site file: $File" }
}

Write-Host "`nALL VALIDATIONS PASSED" -ForegroundColor Green
