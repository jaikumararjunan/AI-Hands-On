param(
  [switch]$Full,
  [switch]$NoBrowser,
  [ValidateSet('Auto','Interactive')]
  [string]$PortMode = 'Auto'
)

$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Compose = Join-Path $Root 'infra\docker-compose.local.yml'
$EnvFile = Join-Path $Root '.env.local'

function Invoke-DockerNative {
  param(
    [string[]]$Arguments,
    [switch]$Quiet,
    [switch]$AllowFailure
  )

  # Windows PowerShell 5 can turn normal Docker stderr progress (for example
  # "Container ... Stopping") into NativeCommandError when
  # $ErrorActionPreference='Stop'. Run native Docker commands with Continue,
  # merge stderr/stdout, and decide success only from the native exit code.
  $previousPreference = $ErrorActionPreference
  try {
    $ErrorActionPreference = 'Continue'
    if ($Quiet) {
      & docker @Arguments 2>&1 | Out-Null
    } else {
      & docker @Arguments 2>&1 | ForEach-Object { Write-Host $_ }
    }
    $exitCode = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $previousPreference
  }

  if ($exitCode -ne 0 -and -not $AllowFailure) {
    throw "Docker command failed with exit code $exitCode: docker $($Arguments -join ' ')"
  }
  return $exitCode
}

function Test-Port([int]$Port) {
  if ($Port -lt 1 -or $Port -gt 65535) { return $false }
  try {
    $listener = [System.Net.Sockets.TcpListener]::new([Net.IPAddress]::Loopback, $Port)
    $listener.Start()
    $listener.Stop()
    return $true
  } catch {
    return $false
  }
}

$UsedPorts = [System.Collections.Generic.HashSet[int]]::new()

function Test-PortAvailable([int]$Port) {
  return (Test-Port $Port) -and (-not $UsedPorts.Contains($Port))
}

function Find-FreePort([int[]]$Candidates, [int]$Preferred) {
  foreach ($candidate in $Candidates) {
    if (Test-PortAvailable $candidate) { return $candidate }
  }
  for ($candidate = [Math]::Max(1024, $Preferred + 1); $candidate -le [Math]::Min(65535, $Preferred + 200); $candidate++) {
    if (Test-PortAvailable $candidate) { return $candidate }
  }
  throw "No free port found near $Preferred."
}

function Select-Port(
  [string]$Service,
  [int]$Preferred,
  [int[]]$Candidates
) {
  $suggested = Find-FreePort $Candidates $Preferred

  if ($PortMode -eq 'Auto') {
    $selected = $suggested
    if ($selected -ne $Preferred) {
      Write-Host ("{0}: preferred port {1} is occupied; automatically using {2}." -f $Service, $Preferred, $selected) -ForegroundColor Yellow
    } else {
      Write-Host ("{0}: using preferred port {1}." -f $Service, $selected) -ForegroundColor DarkGray
    }
  } else {
    Write-Host ""
    Write-Host "[$Service]" -ForegroundColor Cyan
    if (Test-PortAvailable $Preferred) {
      Write-Host "Preferred port $Preferred is available."
    } else {
      Write-Host "Preferred port $Preferred is OCCUPIED." -ForegroundColor Yellow
    }
    Write-Host "Suggested free port: $suggested"

    while ($true) {
      $raw = Read-Host "Enter host port, or press Enter to use $suggested"
      if ([string]::IsNullOrWhiteSpace($raw)) {
        $selected = $suggested
        break
      }

      $candidate = 0
      if (-not [int]::TryParse($raw, [ref]$candidate)) {
        Write-Host "Please enter a number from 1 to 65535." -ForegroundColor Yellow
        continue
      }
      if ($candidate -lt 1 -or $candidate -gt 65535) {
        Write-Host "Port must be from 1 to 65535." -ForegroundColor Yellow
        continue
      }
      if ($UsedPorts.Contains($candidate)) {
        Write-Host "Port $candidate is already selected for another AI Commerce service." -ForegroundColor Yellow
        continue
      }
      if (-not (Test-Port $candidate)) {
        Write-Host "Port $candidate is currently occupied. Choose another port." -ForegroundColor Yellow
        continue
      }
      $selected = $candidate
      break
    }
  }

  [void]$UsedPorts.Add([int]$selected)
  return [int]$selected
}

if (-not (Get-Command docker -ErrorAction SilentlyContinue)) {
  throw 'Docker CLI not found. Install/start Docker Desktop first.'
}

if ((Invoke-DockerNative -Arguments @('info') -Quiet -AllowFailure) -ne 0) {
  throw 'Docker Desktop daemon is not ready.'
}

if ((Invoke-DockerNative -Arguments @('compose','version') -Quiet -AllowFailure) -ne 0) {
  throw 'Docker Compose plugin is unavailable.'
}

# Stop only the previous AI Commerce project. This frees its old host ports while leaving unrelated containers alone.
if (Test-Path $EnvFile) {
  Write-Host 'Stopping previous AI Commerce stack so its ports can be reused...' -ForegroundColor Cyan
  $downArgs = @('compose','--env-file',$EnvFile,'-f',$Compose,'--profile','full','down','--remove-orphans')
  $downExit = Invoke-DockerNative -Arguments $downArgs -Quiet -AllowFailure
  if ($downExit -ne 0) {
    Write-Warning "Previous AI Commerce stack returned exit code $downExit while stopping. Continuing to port checks; any still-bound port will be detected automatically."
  }
}

Write-Host ""
Write-Host "Port selection mode: $PortMode" -ForegroundColor Green
Write-Host "Auto = preferred port first, next free port otherwise."
Write-Host "Interactive = you approve or type every host port."

$ports = [ordered]@{}
$ports.JAVA_PORT          = Select-Port 'Java API'          8080 @(8080,8081,8082,18080)
$ports.AI_PORT            = Select-Port 'Python AI API'     8000 @(8000,8001,8002,18000)
$ports.APP_PORT           = Select-Port 'Commerce application' 9200 @(9200,9201,9202,19200)
$ports.LEARNING_PORT      = Select-Port 'Learning site'        9100 @(9100,9101,9102,19100)
$ports.POSTGRES_PORT      = Select-Port 'PostgreSQL'        5432 @(5432,5433,5434,15432)
$ports.REDIS_PORT         = Select-Port 'Redis'             6379 @(6379,6380,6381,16379)
$ports.QDRANT_PORT        = Select-Port 'Qdrant HTTP'       6333 @(6333,6335,6337,16333)
$ports.QDRANT_GRPC_PORT   = Select-Port 'Qdrant gRPC'       6334 @(6334,6336,6338,16334)
$ports.KAFKA_PORT         = Select-Port 'Kafka host'        9092 @(9092,9094,9096,19092)

if ($Full) {
  $ports.MLFLOW_PORT        = Select-Port 'MLflow'            5000 @(5000,5001,5002,15000)
  $ports.PROMETHEUS_PORT    = Select-Port 'Prometheus'        9090 @(9090,9091,9093,19090)
  $ports.GRAFANA_PORT       = Select-Port 'Grafana'           3000 @(3000,3001,3002,13000)
  $ports.OTEL_GRPC_PORT     = Select-Port 'OTel gRPC'         4317 @(4317,14317,24317)
  $ports.OTEL_HTTP_PORT     = Select-Port 'OTel HTTP'         4318 @(4318,14318,24318)
  $ports.OTEL_METRICS_PORT  = Select-Port 'OTel metrics'      9464 @(9464,19464,29464)
} else {
  $ports.MLFLOW_PORT       = 5000
  $ports.PROMETHEUS_PORT   = 9090
  $ports.GRAFANA_PORT      = 3000
  $ports.OTEL_GRPC_PORT    = 4317
  $ports.OTEL_HTTP_PORT    = 4318
  $ports.OTEL_METRICS_PORT = 9464
}

$ports.GetEnumerator() | ForEach-Object { "$($_.Key)=$($_.Value)" } | Set-Content -Encoding ascii $EnvFile
"OLLAMA_BASE_URL=http://host.docker.internal:11434" | Add-Content $EnvFile
"OLLAMA_MODEL=llama3.2:3b" | Add-Content $EnvFile
if ($Full) {
  "OTEL_EXPORTER_OTLP_ENDPOINT=http://otel-collector:4317" | Add-Content $EnvFile
} else {
  "OTEL_EXPORTER_OTLP_ENDPOINT=" | Add-Content $EnvFile
}

Write-Host ""
Write-Host 'Selected host ports:' -ForegroundColor Cyan
$ports.GetEnumerator() | ForEach-Object { Write-Host ("  {0,-22} {1}" -f $_.Key, $_.Value) }
Write-Host "Saved to: $EnvFile"

$args = @('compose','--env-file',$EnvFile,'-f',$Compose)
if ($Full) { $args += @('--profile','full') }
$args += @('up','-d','--build','--remove-orphans')

$upExit = Invoke-DockerNative -Arguments $args -AllowFailure
if ($upExit -ne 0) {
  Write-Host ""
  Write-Host 'Docker compose failed. Collecting diagnostics...' -ForegroundColor Red
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'--profile','full','ps','-a') -AllowFailure)
  Write-Host ''
  Write-Host '=== AI PYTHON LOGS ===' -ForegroundColor Cyan
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'logs','--tail','120','ai-python') -AllowFailure)
  Write-Host ''
  Write-Host '=== JAVA LOGS ===' -ForegroundColor Cyan
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'logs','--tail','160','commerce-java') -AllowFailure)
  throw 'Docker deployment failed. Diagnostics are shown above. You can also run DOCKER_STATUS.bat.'
}

function Wait-Http([string]$Url, [int]$Attempts = 75) {
  for ($i = 0; $i -lt $Attempts; $i++) {
    try {
      $response = Invoke-WebRequest -UseBasicParsing -Uri $Url -TimeoutSec 3
      if ($response.StatusCode -ge 200 -and $response.StatusCode -lt 500) { return $true }
    } catch {}
    Start-Sleep -Seconds 2
  }
  return $false
}

$aiHealthy = Wait-Http "http://localhost:$($ports.AI_PORT)/health"
if (-not $aiHealthy) {
  Write-Warning 'Python health endpoint is not ready. Showing Python container diagnostics now.'
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'ps','-a','ai-python') -AllowFailure)
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'logs','--tail','160','ai-python') -AllowFailure)
}

$javaHealthy = Wait-Http "http://localhost:$($ports.JAVA_PORT)/actuator/health"
$appHealthy = Wait-Http "http://localhost:$($ports.APP_PORT)" 45
if (-not $javaHealthy) {
  Write-Warning 'Java health endpoint is not ready. Showing Java container diagnostics now.'
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'ps','-a','commerce-java') -AllowFailure)
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'logs','--tail','120','commerce-java') -AllowFailure)
}

if (-not $appHealthy) {
  Write-Warning 'Commerce application URL is not ready. Showing app container diagnostics now.'
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'ps','-a','commerce-app') -AllowFailure)
  [void](Invoke-DockerNative -Arguments @('compose','--env-file',$EnvFile,'-f',$Compose,'logs','--tail','100','commerce-app') -AllowFailure)
}

Write-Host ""
Write-Host 'AI Commerce local deployment started.' -ForegroundColor Green
Write-Host "APPLICATION:  http://localhost:$($ports.APP_PORT)" -ForegroundColor Yellow
Write-Host "Learning:     http://localhost:$($ports.LEARNING_PORT)"
Write-Host "Java health:  http://localhost:$($ports.JAVA_PORT)/actuator/health"
Write-Host "Python docs:  http://localhost:$($ports.AI_PORT)/docs"
Write-Host "Python health:http://localhost:$($ports.AI_PORT)/health"
Write-Host "Qdrant:       http://localhost:$($ports.QDRANT_PORT)/dashboard"
if ($Full) {
  Write-Host "Grafana:      http://localhost:$($ports.GRAFANA_PORT)"
  Write-Host "Prometheus:   http://localhost:$($ports.PROMETHEUS_PORT)"
  Write-Host "MLflow:       http://localhost:$($ports.MLFLOW_PORT)"
}
Write-Host "Ports saved to $EnvFile"
"http://localhost:$($ports.APP_PORT)" | Set-Content -Encoding ascii (Join-Path $Root 'APPLICATION_URL.txt')
"http://localhost:$($ports.LEARNING_PORT)" | Set-Content -Encoding ascii (Join-Path $Root 'LEARNING_URL.txt')

if (-not $NoBrowser) {
  Start-Process "http://localhost:$($ports.APP_PORT)"
}
