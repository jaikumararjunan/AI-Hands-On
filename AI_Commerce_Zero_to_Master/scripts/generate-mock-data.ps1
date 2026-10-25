param(
    [ValidateSet("tiny", "small", "medium", "large", "xlarge")]
    [string]$Profile = "tiny",

    [ValidateSet("normal", "peak-sale", "fraud-attack", "inventory-shortage", "payment-degradation", "returns-spike", "marketing-campaign", "mixed-chaos")]
    [string]$Scenario = "normal",

    [int]$Seed = 42,
    [int]$Days = 180,
    [switch]$SyncDataPlatform
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
$Generator = Join-Path $Root "mock-data\generate_mock_data.py"
$Validator = Join-Path $Root "mock-data\validate_mock_data.py"

$argsList = @(
    $Generator,
    "--profile", $Profile,
    "--scenario", $Scenario,
    "--seed", $Seed,
    "--days", $Days,
    "--reset"
)

if ($SyncDataPlatform) {
    $argsList += "--sync-data-platform"
}

Write-Host "Generating AI Commerce mock data..."
python @argsList

Write-Host ""
Write-Host "Validating referential integrity..."
python $Validator

Write-Host ""
Write-Host "Mock data ready: $Root\mock-data\output\latest"
