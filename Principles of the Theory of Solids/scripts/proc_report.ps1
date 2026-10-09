Get-Process | Sort-Object WS -Descending |
  Select-Object -First 20 Name, Id,
    @{n='WS_MB';e={[math]::Round($_.WS/1MB)}},
    @{n='CPU_s';e={[math]::Round($_.CPU)}} |
  Format-Table -AutoSize
"---- python/xelatex/bash processes ----"
Get-Process -Name python,xelatex,bash,sh,node -ErrorAction SilentlyContinue |
  Select-Object Name, Id, @{n='WS_MB';e={[math]::Round($_.WS/1MB)}},
    @{n='CPU_s';e={[math]::Round($_.CPU)}}, StartTime |
  Format-Table -AutoSize
"---- total memory ----"
$os = Get-CimInstance Win32_OperatingSystem
"Free {0:N1} GB / Total {1:N1} GB" -f ($os.FreePhysicalMemory/1MB), ($os.TotalVisibleMemorySize/1MB)
