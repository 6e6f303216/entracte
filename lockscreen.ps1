function Start-Break {
    param([int]$sleepTime)
    
    $minutes = [math]::Floor($sleepTime / 60)
    
    $shell = New-Object -ComObject Shell.Application
    $shell.MinimizeAll()

    Start-Sleep -Seconds $sleepTime

    $shell.UndoMinimizeAll()
}

if ($args[0] -eq "break") {
    Start-Break $args[1]
}
else {
    Write-Host "Usage: lockscreen.ps1 {break|work} [SLEEP_TIME]"
}
