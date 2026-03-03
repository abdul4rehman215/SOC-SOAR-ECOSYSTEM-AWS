param([string]$domain)

$apiKey = "YOUR_API_KEY"
$url = "https://otx.alienvault.com/api/v1/indicators/domain/$domain/general"

$headers = @{
    "X-OTX-API-KEY" = $apiKey
}

$response = Invoke-RestMethod -Uri $url -Headers $headers -Method Get

if ($response.pulse_info.count -gt 0) {
    Write-Output "Malicious domain found in OTX"
}
