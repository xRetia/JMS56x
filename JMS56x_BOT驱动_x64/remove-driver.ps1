$out = pnputil /enum-drivers
$oem = $null
for ($i = 0; $i -lt $out.Count; $i++) {
    if ($out[$i] -match "Published Name:\s+(oem\d+\.inf)") {
        $pub = $matches[1]
        for ($j = $i+1; $j -lt [Math]::Min($i+5, $out.Count); $j++) {
            if ($out[$j] -match "jms56xbot\.inf") {
                $oem = $pub
                break
            }
        }
    }
    if ($oem) { break }
}
if ($oem) {
    Write-Host "Removing: $oem"
    pnputil /delete-driver $oem /uninstall /force
} else {
    Write-Host "Driver package not found (already removed?)"
}