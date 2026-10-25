$ErrorActionPreference='Stop'
$Root=(Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$Compose=Join-Path $Root 'infra\docker-compose.local.yml'
$Env=Join-Path $Root '.env.local'

function Invoke-DockerDown([string[]]$Arguments) {
  $previousPreference = $ErrorActionPreference
  try {
    $ErrorActionPreference = 'Continue'
    & docker @Arguments 2>&1 | ForEach-Object { Write-Host $_ }
    $exitCode = $LASTEXITCODE
  } finally {
    $ErrorActionPreference = $previousPreference
  }
  if ($exitCode -ne 0) { throw "Docker stop failed with exit code $exitCode." }
}

if(Test-Path $Env){
  Invoke-DockerDown -Arguments @('compose','--env-file',$Env,'-f',$Compose,'--profile','full','down','--remove-orphans')
} else {
  Invoke-DockerDown -Arguments @('compose','-f',$Compose,'--profile','full','down','--remove-orphans')
}
