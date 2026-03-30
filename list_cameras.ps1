Add-Type -AssemblyName System.Runtime.WindowsRuntime
Add-Type -AssemblyName Windows.Media.Capture

# Use WinRT async operation
$null = [Windows.Media.Capture.MediaCapture, Windows.Media.Capture, ContentType = WindowsRuntime]
$null = [Windows.Foundation.IAsyncOperation`1, Windows.Foundation, ContentType = WindowsRuntime]

Write-Host "Checking available cameras..."

try {
    $asyncOp = [Windows.Media.Capture.MediaCapture]::FindAllAsync()
    $task = [System.Threading.Tasks.Task]::FromResult($asyncOp)
    $devices = $task.Result
    
    Write-Host "Found cameras:"
    foreach ($d in $devices) {
        Write-Host "  -" $d.Name
    }
} catch {
    Write-Host "Error: $_"
}
