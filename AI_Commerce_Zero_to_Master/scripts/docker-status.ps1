$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Compose = Join-Path $Root 'infra\docker-compose.local.yml'
$Env = Join-Path $Root '.env.local'

if (!(Test-Path $Env)) {
  Write-Host 'No .env.local yet. Start the stack first.'
  exit 1
}

Write-Host '=== SELECTED HOST PORTS ===' -ForegroundColor Cyan
Get-Content $Env | Where-Object { $_ -match '_PORT=' }

$envMap = @{}
Get-Content $Env | ForEach-Object {
  if ($_ -match '^([^=]+)=(.*)$') { $envMap[$matches[1]] = $matches[2] }
}
Write-Host ''
Write-Host '=== APPLICATION LINKS ===' -ForegroundColor Cyan
if ($envMap['APP_PORT']) { Write-Host ('Application: http://localhost:' + $envMap['APP_PORT']) -ForegroundColor Yellow }
if ($envMap['LEARNING_PORT']) { Write-Host ('Learning:    http://localhost:' + $envMap['LEARNING_PORT']) }
if ($envMap['JAVA_PORT']) { Write-Host ('Java API:    http://localhost:' + $envMap['JAVA_PORT'] + '/actuator/health') }
if ($envMap['AI_PORT']) { Write-Host ('Python API:  http://localhost:' + $envMap['AI_PORT'] + '/docs') }

Write-Host ''
Write-Host '=== CONTAINER STATUS ===' -ForegroundColor Cyan
docker compose --env-file $Env -f $Compose --profile full ps -a
Write-Host ''
Write-Host '=== AI PYTHON LOGS ===' -ForegroundColor Cyan
docker compose --env-file $Env -f $Compose logs --tail 100 ai-python
Write-Host ''
Write-Host '=== JAVA LOGS ===' -ForegroundColor Cyan
docker compose --env-file $Env -f $Compose logs --tail 80 commerce-java

Write-Host ''
Write-Host '=== COMMERCE APP LOGS ===' -ForegroundColor Cyan
docker compose --env-file $Env -f $Compose logs --tail 60 commerce-app
