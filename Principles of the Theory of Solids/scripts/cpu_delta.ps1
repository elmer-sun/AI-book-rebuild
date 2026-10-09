$a = Get-Process | Select-Object Name, Id, CPU
Start-Sleep -Seconds 4
$b = Get-Process | Select-Object Name, Id, CPU
$rows = foreach ($p in $b) {
  $o = $a | Where-Object { $_.Id -eq $p.Id }
  if ($o -and ($null -ne $p.CPU) -and ($null -ne $o.CPU)) {
    $delta = $p.CPU - $o.CPU
    if ($delta -gt 0.15) {
      [pscustomobject]@{ Name = $p.Name; Id = $p.Id; CPU_pct = [math]::Round($delta / 4 * 100) }
    }
  }
}
$rows | Sort-Object CPU_pct -Descending | Select-Object -First 12 | Format-Table -AutoSize
