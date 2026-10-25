$ErrorActionPreference = "Stop"
Write-Host "Checking Python AI service..."
Invoke-RestMethod http://localhost:8000/health | ConvertTo-Json
Write-Host "Searching for AI laptop..."
Invoke-RestMethod "http://localhost:8000/ai/search?q=laptop%20for%20AI&limit=3" | ConvertTo-Json -Depth 5
Write-Host "Checking Java commerce service..."
Invoke-RestMethod http://localhost:8080/actuator/health | ConvertTo-Json -Depth 5
Write-Host "Listing products..."
Invoke-RestMethod http://localhost:8080/api/products | ConvertTo-Json -Depth 5
Write-Host "Creating sample order..."
$body = @{customerId='C100'; couponCode='WELCOME10'; items=@(@{productId='P100';quantity=1},@{productId='P500';quantity=1})} | ConvertTo-Json -Depth 5
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/orders -ContentType 'application/json' -Body $body | ConvertTo-Json -Depth 5
Write-Host "Asking commerce agent..."
$ask = @{question='Find a laptop for local AI and explain the return policy'} | ConvertTo-Json
Invoke-RestMethod -Method Post -Uri http://localhost:8080/api/ai/ask -ContentType 'application/json' -Body $ask | ConvertTo-Json -Depth 5
