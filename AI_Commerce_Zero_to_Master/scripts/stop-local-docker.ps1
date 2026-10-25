$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Compose=Join-Path $Root 'infra\docker-compose.local.yml'
$Env=Join-Path $Root '.env.local'
if(Test-Path $Env){ docker compose --env-file $Env -f $Compose --profile full down --remove-orphans } else { docker compose -f $Compose --profile full down --remove-orphans }
