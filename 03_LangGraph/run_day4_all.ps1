$ErrorActionPreference = "Stop"


Write-Host ""
Write-Host "============================================"
Write-Host " DAY 4 - LANGGRAPH FULL TEST"
Write-Host "============================================"
Write-Host ""


# ============================================================
# CHECK PYTHON
# ============================================================

Write-Host "Checking Python..."

python --version

if ($LASTEXITCODE -ne 0) {

    throw "Python is not available."
}


# ============================================================
# CHECK DATASET
# ============================================================

$dataFile = "..\01_Python_DataScience\sales_100k_raw.csv"


Write-Host ""
Write-Host "Checking dataset..."


if (-not (Test-Path $dataFile)) {

    throw "Dataset not found: $dataFile"
}


Write-Host "Dataset found."


# ============================================================
# CHECK OLLAMA
# ============================================================

Write-Host ""
Write-Host "Checking Ollama..."


ollama --version


if ($LASTEXITCODE -ne 0) {

    throw "Ollama is unavailable."
}


# ============================================================
# FILES
# ============================================================

$scripts = @(

    "01_state_basic.py",

    "02_nodes_edges.py",

    "03_conditional_routing.py",

    "04_sales_graph.py",

    "05_langchain_graph.py",

    "06_ml_graph.py",

    "07_full_enterprise_graph.py"
)


# ============================================================
# RUN
# ============================================================

foreach ($script in $scripts) {

    Write-Host ""

    Write-Host "============================================"

    Write-Host "RUNNING: $script"

    Write-Host "============================================"


    if (-not (Test-Path $script)) {

        throw "Missing script: $script"
    }


    python $script


    if ($LASTEXITCODE -ne 0) {

        Write-Host ""

        Write-Host "FAILED: $script"

        exit $LASTEXITCODE
    }


    Write-Host ""

    Write-Host "PASSED: $script"
}


Write-Host ""

Write-Host "============================================"

Write-Host " ALL DAY 4 SCRIPTS PASSED"

Write-Host "============================================"