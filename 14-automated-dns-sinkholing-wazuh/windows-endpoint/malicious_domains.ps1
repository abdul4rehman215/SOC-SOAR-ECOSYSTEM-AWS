#############################################
# Wazuh Automated DNS Sinkhole Script
#############################################

$log = "C:\Windows\Temp\sinkhole.log"

"---------------------------------------" | Out-File -Append $log
"Execution Time: $(Get-Date)" | Out-File -Append $log

# Read JSON input from Wazuh
$INPUT_JSON = Read-Host
$INPUT_ARRAY = $INPUT_JSON | ConvertFrom-Json
$INPUT_ARRAY = $INPUT_ARRAY | ConvertFrom-Json

# Extract malicious domain from OTX alert
$malicious_domain = $INPUT_ARRAY.parameters.alert.data.base_indicator.indicator

if (-not $malicious_domain) {
    "No malicious domain found in alert" | Out-File -Append $log
    exit 0
}

"Malicious domain detected: $malicious_domain" | Out-File -Append $log

# Hosts file location
$hosts_file = "$env:windir\System32\drivers\etc\hosts"

# Prevent duplicate entries
if (Select-String -Path $hosts_file -Pattern $malicious_domain -Quiet) {
    "Domain already sinkholed" | Out-File -Append $log
    exit 0
}

# Add sinkhole entry
Add-Content -Path $hosts_file -Value "`n127.0.0.1`t$malicious_domain" -Force

"Domain sinkholed successfully" | Out-File -Append $log
