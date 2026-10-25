$ErrorActionPreference = "Stop"

$checkout = @{
  order = @{
    customerId = "CUST-101"
    couponCode = "WELCOME10"
    items = @(
      @{ productId = "P100"; quantity = 1 }
    )
  }
  currency = "INR"
  paymentMethodRef = "pm_mock_token_123"
} | ConvertTo-Json -Depth 6

$idempotencyKey = [guid]::NewGuid().ToString()

$result = Invoke-RestMethod `
  -Uri "http://localhost:8080/api/checkout" `
  -Method Post `
  -ContentType "application/json" `
  -Headers @{"Idempotency-Key" = $idempotencyKey} `
  -Body $checkout

$result | ConvertTo-Json -Depth 8

$paymentId = $result.payment.paymentId
Write-Host "Payment ID: $paymentId"

Invoke-RestMethod -Uri "http://localhost:8080/api/payments/$paymentId/confirm" -Method Post | ConvertTo-Json -Depth 6
Invoke-RestMethod -Uri "http://localhost:8080/api/payments/$paymentId/capture" -Method Post | ConvertTo-Json -Depth 6
