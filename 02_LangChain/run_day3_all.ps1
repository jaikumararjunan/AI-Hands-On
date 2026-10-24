$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================"
Write-Host " DAY 3 - LANGCHAIN FULL TEST"
Write-Host "============================================"
Write-Host ""

# ---------------------------------------------------
# STEP 1 - CHECK PYTHON
# ---------------------------------------------------

Write-Host "Checking Python..."

python --version

if ($LASTEXITCODE -ne 0) {
    throw "Python is not available."
}

# ---------------------------------------------------
# STEP 2 - CHECK OLLAMA
# ---------------------------------------------------

Write-Host ""
Write-Host "Checking Ollama..."

ollama --version

if ($LASTEXITCODE -ne 0) {
    throw "Ollama is not available."
}

# ---------------------------------------------------
# STEP 3 - CHECK MODEL
# ---------------------------------------------------

Write-Host ""
Write-Host "Checking llama3.2:3b..."

$modelFound = ollama list |
    Select-String "llama3.2:3b"

if (-not $modelFound) {

    Write-Host "Model not found."
    Write-Host "Pulling llama3.2:3b..."

    ollama pull llama3.2:3b
}

# ---------------------------------------------------
# STEP 4 - CHECK DATASET
# ---------------------------------------------------

$dataFile = "..\01_Python_DataScience\sales_100k_raw.csv"

Write-Host ""
Write-Host "Checking dataset..."

if (-not (Test-Path $dataFile)) {

    throw "Dataset not found: $dataFile"
}

Write-Host "Dataset found."

# ---------------------------------------------------
# STEP 5 - RUN DAY 3
# ---------------------------------------------------

$scripts = @(
    "01_test_ollama.py",
    "02_langchain_model.py",
    "03_prompt.py",
    "04_structured_output.py",
    "05_tools.py",
    "06_test_sales_tools.py",
    "07_tool_calling.py",
    "08_agent.py",
    "09_final_demo.py"
)

foreach ($script in $scripts) {

    Write-Host ""
    Write-Host "============================================"
    Write-Host "RUNNING: $script"
    Write-Host "============================================"

    if (-not (Test-Path $script)) {

        Write-Host "SKIPPED - file not found: $script"
        continue
    }

    python $script

    if ($LASTEXITCODE -ne 0) {

        Write-Host ""
        Write-Host "FAILED: $script"
        Write-Host ""
        Write-Host "Fix this script before continuing."

        exit $LASTEXITCODE
    }

    Write-Host ""
    Write-Host "PASSED: $script"
}

Write-Host ""
Write-Host "============================================"
Write-Host " DAY 3 COMPLETE"
Write-Host "============================================"