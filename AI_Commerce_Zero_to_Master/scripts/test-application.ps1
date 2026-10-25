$ErrorActionPreference = 'Stop'
$Root = (Resolve-Path (Join-Path $PSScriptRoot '..')).Path
$EnvFile = Join-Path $Root '.env.local'

if (-not (Test-Path $EnvFile)) {
  throw 'Missing .env.local. Start the Docker stack first.'
}

$envMap = @{}
Get-Content $EnvFile | ForEach-Object {
  $line = $_.Trim()
  if ($line -and -not $line.StartsWith('#') -and $line.Contains('=')) {
    $parts = $line.Split('=', 2)
    $envMap[$parts[0]] = $parts[1]
  }
}

function Get-Port([string]$Name, [int]$Default) {
  if ($envMap.ContainsKey($Name) -and $envMap[$Name]) { return [int]$envMap[$Name] }
  return $Default
}

$AppPort = Get-Port 'APP_PORT' 9200
$JavaPort = Get-Port 'JAVA_PORT' 8080
$AiPort = Get-Port 'AI_PORT' 8000
$AppBase = "http://localhost:$AppPort"
$JavaBase = "http://localhost:$JavaPort"
$AiBase = "http://localhost:$AiPort"
$Customer = 'E2E-' + ([guid]::NewGuid().ToString('N').Substring(0,8))
$Results = [System.Collections.Generic.List[object]]::new()

function Add-Result([string]$Name, [bool]$Passed, [string]$Detail) {
  $Results.Add([pscustomobject]@{ Test=$Name; Status=($(if($Passed){'PASS'}else{'FAIL'})); Detail=$Detail }) | Out-Null
  if ($Passed) { Write-Host ("[PASS] {0} - {1}" -f $Name, $Detail) -ForegroundColor Green }
  else { Write-Host ("[FAIL] {0} - {1}" -f $Name, $Detail) -ForegroundColor Red }
}

function Run-Test([string]$Name, [scriptblock]$Body) {
  try {
    $detail = & $Body
    if ($null -eq $detail) { $detail = 'OK' }
    Add-Result $Name $true ([string]$detail)
  } catch {
    Add-Result $Name $false $_.Exception.Message
  }
}

Write-Host '============================================================'
Write-Host 'AI COMMERCE - END TO END APPLICATION TEST'
Write-Host '============================================================'
Write-Host ("Application : {0}" -f $AppBase)
Write-Host ("Java API    : {0}" -f $JavaBase)
Write-Host ("Python API  : {0}" -f $AiBase)
Write-Host ''

Run-Test 'Storefront HTML' {
  $r = Invoke-WebRequest -UseBasicParsing -Uri $AppBase -TimeoutSec 10
  if ($r.StatusCode -ne 200 -or $r.Content -notmatch 'AI Commerce Store') { throw 'Storefront did not return expected HTML.' }
  'HTTP 200 and storefront marker found'
}

Run-Test 'Java health through storefront' {
  $r = Invoke-RestMethod -Uri "$AppBase/java-health" -TimeoutSec 10
  if ($r.status -ne 'UP') { throw "Java health status was $($r.status)" }
  'status=UP'
}

Run-Test 'Python health through storefront' {
  $r = Invoke-RestMethod -Uri "$AppBase/python/health" -TimeoutSec 10
  if ($r.status -ne 'UP') { throw "Python health status was $($r.status)" }
  'status=UP'
}

Run-Test 'Python OpenAPI through storefront' {
  $doc = Invoke-RestMethod -Uri "$AppBase/python/openapi.json" -TimeoutSec 10
  if (-not $doc.openapi) { throw 'Missing OpenAPI version field.' }
  if (-not ($doc.paths.PSObject.Properties.Name -contains '/ai/agent/ask')) { throw 'OpenAPI is missing /ai/agent/ask.' }
  "openapi=$($doc.openapi)"
}

Run-Test 'Python Swagger through storefront' {
  $r = Invoke-WebRequest -UseBasicParsing -Uri "$AppBase/python/docs" -TimeoutSec 10
  if ($r.StatusCode -ne 200 -or $r.Content -notmatch 'swagger-ui') { throw 'Swagger HTML was not rendered.' }
  if ($r.Content -notmatch '/python/openapi.json') { throw 'Swagger is not pointing to the proxied /python/openapi.json path.' }
  'Swagger uses /python/openapi.json'
}

$catalog = $null
Run-Test 'Product catalog' {
  $script:catalog = Invoke-RestMethod -Uri "$AppBase/api/products" -TimeoutSec 10
  if (-not $script:catalog -or $script:catalog.Count -lt 1) { throw 'Catalog is empty.' }
  "$($script:catalog.Count) products"
}

Run-Test 'AI semantic search Java to Python' {
  $r = Invoke-RestMethod -Uri "$AppBase/api/ai/search?q=laptop" -TimeoutSec 15
  if (-not $r.results) { throw 'Search returned no results.' }
  "$($r.results.Count) results"
}

Run-Test 'AI recommendations Java to Python' {
  $r = Invoke-RestMethod -Uri "$AppBase/api/ai/recommendations/C100" -TimeoutSec 15
  if (-not $r.recommendations) { throw 'Recommendations returned no rows.' }
  "$($r.recommendations.Count) recommendations"
}

$AskBody = @{ question='I need a laptop for local AI development and a monitor. What should I consider?' } | ConvertTo-Json
Run-Test 'Direct Python agent contract' {
  $r = Invoke-RestMethod -Method Post -Uri "$AiBase/ai/agent/ask" -ContentType 'application/json' -Body $AskBody -TimeoutSec 30
  if (-not $r.answer) { throw 'Python agent returned no answer.' }
  if ($r.route -eq 'error') { throw 'Python agent returned route=error.' }
  "route=$($r.route), degraded=$($r.degraded)"
}

Run-Test 'Ask AI through storefront Java proxy' {
  $r = Invoke-RestMethod -Method Post -Uri "$AppBase/api/ai/ask" -ContentType 'application/json' -Body $AskBody -TimeoutSec 30
  if ($r.downstreamStatus -eq 422) { throw "Python rejected Java request with 422. Body: $($r.downstreamBody)" }
  if (-not $r.answer) { throw 'Ask AI returned no answer.' }
  if ($r.route -eq 'error') { throw "Ask AI route=error. Diagnostic=$($r.diagnostic) Body=$($r.downstreamBody)" }
  "route=$($r.route), degraded=$($r.degraded)"
}

$productId = 'P100'
if ($catalog -and $catalog.Count -gt 0) {
  $candidate = $catalog[0]
  if ($candidate.productId) { $productId = $candidate.productId }
  elseif ($candidate.id) { $productId = $candidate.id }
}

Run-Test 'Cart add and read' {
  $body = @{ productId=$productId; quantity=1 } | ConvertTo-Json
  $null = Invoke-RestMethod -Method Post -Uri "$AppBase/api/carts/$Customer/items" -ContentType 'application/json' -Body $body -TimeoutSec 10
  $cart = Invoke-RestMethod -Uri "$AppBase/api/carts/$Customer" -TimeoutSec 10
  if (-not $cart.items -or $cart.items.Count -lt 1) { throw 'Cart did not contain the added item.' }
  "customer=$Customer product=$productId"
}

$checkoutResult = $null
Run-Test 'Checkout and payment intent' {
  $payload = @{
    order = @{ customerId=$Customer; items=@(@{productId=$productId; quantity=1}); couponCode=$null }
    currency = 'INR'
    paymentMethodRef = 'tok_e2e_visa'
  } | ConvertTo-Json -Depth 8
  $key = 'e2e-' + [guid]::NewGuid().ToString('N')
  $script:checkoutResult = Invoke-RestMethod -Method Post -Uri "$AppBase/api/checkout" -Headers @{'Idempotency-Key'=$key} -ContentType 'application/json' -Body $payload -TimeoutSec 15
  if (-not $script:checkoutResult.order.orderId) { throw 'Checkout did not create an order.' }
  if (-not $script:checkoutResult.payment.paymentId) { throw 'Checkout did not create a payment intent.' }
  "order=$($script:checkoutResult.order.orderId), payment=$($script:checkoutResult.payment.paymentId)"
}

Run-Test 'Payment confirm and capture' {
  if (-not $checkoutResult.payment.paymentId) { throw 'No paymentId available from checkout.' }
  $payment = $checkoutResult.payment
  if ($payment.status -eq 'REQUIRES_ACTION') {
    $payment = Invoke-RestMethod -Method Post -Uri "$AppBase/api/payments/$($payment.paymentId)/confirm" -TimeoutSec 10
  }
  if ($payment.status -eq 'AUTHORIZED') {
    $payment = Invoke-RestMethod -Method Post -Uri "$AppBase/api/payments/$($payment.paymentId)/capture" -TimeoutSec 10
  }
  if ($payment.status -ne 'CAPTURED') { throw "Expected CAPTURED payment but got $($payment.status)" }
  'status=CAPTURED'
}

Run-Test 'Vector index via storefront Python proxy' {
  $r = Invoke-RestMethod -Method Post -Uri "$AppBase/python/ai/vector/index" -TimeoutSec 30
  if (-not $r.documents) { throw 'Vector index reported no documents.' }
  "documents=$($r.documents), backend=$($r.backend)"
}

Run-Test 'Vector search via storefront Python proxy' {
  $r = Invoke-RestMethod -Uri "$AppBase/python/ai/vector/search?q=return%20policy&limit=3" -TimeoutSec 30
  if (-not $r.results) { throw 'Vector search returned no results.' }
  "$($r.results.Count) vector results"
}

Run-Test 'Grounded RAG answer' {
  $r = Invoke-RestMethod -Uri "$AppBase/python/ai/rag/answer?q=What%20is%20the%20return%20policy%3F&limit=3" -TimeoutSec 45
  if (-not $r.answer) { throw 'RAG returned no answer.' }
  if (-not $r.sources) { throw 'RAG returned no sources.' }
  "sources=$($r.sources.Count)"
}

Run-Test 'Cart cleanup' {
  Invoke-RestMethod -Method Delete -Uri "$AppBase/api/carts/$Customer" -TimeoutSec 10 | Out-Null
  $cart = Invoke-RestMethod -Uri "$AppBase/api/carts/$Customer" -TimeoutSec 10
  if ($cart.items -and $cart.items.Count -gt 0) { throw 'Cart cleanup failed.' }
  'cart empty'
}

Write-Host ''
Write-Host '==================== TEST SUMMARY ==========================='
$Results | Format-Table -AutoSize
$failed = @($Results | Where-Object { $_.Status -eq 'FAIL' })
Write-Host ("Passed: {0}  Failed: {1}  Total: {2}" -f ($Results.Count-$failed.Count), $failed.Count, $Results.Count)
if ($failed.Count -gt 0) {
  Write-Host 'APPLICATION TEST FAILED' -ForegroundColor Red
  exit 1
}
Write-Host 'APPLICATION TEST PASSED' -ForegroundColor Green
exit 0
