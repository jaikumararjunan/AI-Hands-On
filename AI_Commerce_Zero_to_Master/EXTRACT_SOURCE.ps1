$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Payload = Join-Path $Root 'source-payload'
$Destination = Join-Path $Root 'expanded'
$B64File = Join-Path $env:TEMP 'ai-commerce-source.b64'
$Archive = Join-Path $env:TEMP 'ai-commerce-source.tar.xz'

Write-Host '============================================================'
Write-Host ' AI COMMERCE ZERO TO MASTER - EXTRACT COMPLETE SOURCE'
Write-Host '============================================================'

$parts = Get-ChildItem -Path $Payload -Recurse -Filter 'part-*.b64' | Sort-Object FullName
if ($parts.Count -ne 14) {
    throw "Expected 14 payload parts, found $($parts.Count)."
}

$builder = New-Object System.Text.StringBuilder
foreach ($part in $parts) {
    [void]$builder.Append((Get-Content -Raw -Path $part.FullName).Trim())
}
[System.IO.File]::WriteAllText($B64File, $builder.ToString())
$bytes = [Convert]::FromBase64String($builder.ToString())
[System.IO.File]::WriteAllBytes($Archive, $bytes)

$hash = (Get-FileHash -Algorithm SHA256 $Archive).Hash.ToLowerInvariant()
$expected = 'f41aabe4384d3975d3f98ef76ee503946e2830104975edb0c0295ada1051bbc2'
if ($hash -ne $expected) {
    throw "Payload checksum mismatch. Expected $expected, got $hash"
}

if (Test-Path $Destination) { Remove-Item -Recurse -Force $Destination }
New-Item -ItemType Directory -Path $Destination | Out-Null
& tar -xJf $Archive -C $Destination
if ($LASTEXITCODE -ne 0) { throw 'tar extraction failed.' }

$Project = Join-Path $Destination 'AI_Commerce_Zero_to_Master'
if (-not (Test-Path (Join-Path $Project 'README.md'))) { throw 'Extracted project validation failed.' }

Write-Host ''
Write-Host 'Complete source extracted successfully:'
Write-Host $Project
Write-Host ''
Write-Host 'Recommended next step:'
Write-Host "  cd `"$Project`""
Write-Host '  START_FULL_LOCAL_DOCKER_INTERACTIVE.bat'
