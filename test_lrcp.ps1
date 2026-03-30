# Try to access LRCP H-720P via Windows Media Foundation
Add-Type -AssemblyName System.Runtime.WindowsRuntime
Add-Type -AssemblyName Windows.Media.Capture

# Create async operation for finding devices
[Windows.Media.Capture.MediaCapture]$mediaCapture = New-Object Windows.Media.Capture.MediaCapture
$asyncOp = [Windows.Media.Capture.MediaCapture, Windows.Media.Capture, ContentType = WindowsRuntime]::FindAllAsync()

# Wait for completion
$task = [System.Threading.Tasks.Task]::FromResult($asyncOp)
$devices = $task.Result

Write-Host "Found $($devices.Count) camera(s):"
foreach ($d in $devices) {
    Write-Host "  - $($d.Name)"
}

# Try to capture from LRCP
Write-Host "`nAttempting to access cameras..."
