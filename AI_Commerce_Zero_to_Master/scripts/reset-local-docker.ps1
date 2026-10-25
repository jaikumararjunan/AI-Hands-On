param([switch]$Yes)
$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Compose=Join-Path $Root 'infra\docker-compose.local.yml'
$Env=Join-Path $Root '.env.local'
if(!(Test-Path $Env)){throw 'No .env.local found.'}
if(-not $Yes){
  $a=Read-Host 'This deletes AI Commerce Docker volumes/data. Type RESET'
  if($a -ne 'RESET'){exit}
}
$previousPreference=$ErrorActionPreference
try {
  $ErrorActionPreference='Continue'
  & docker compose --env-file $Env -f $Compose --profile full down -v --remove-orphans 2>&1 | ForEach-Object { Write-Host $_ }
  $exitCode=$LASTEXITCODE
} finally {
  $ErrorActionPreference=$previousPreference
}
if($exitCode -ne 0){throw "Docker reset failed with exit code $exitCode."}
