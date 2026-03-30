"""
Try to access LRCP H-720P camera using various methods
"""
import cv2
import subprocess
import numpy as np
from datetime import datetime

def get_usb_device_path():
    """Get the USB device path for LRCP H-720P"""
    result = subprocess.run(
        ['powershell', '-Command', 
         'Get-WmiObject Win32_PnPEntity | Where-Object {$_.Name -like "*LRCP*"} | Select-Object -ExpandProperty DeviceID'],
        capture_output=True, text=True
    )
    return result.stdout.strip()

def try_direct_device_path():
    """Try to open camera using USB device path"""
    device_id = get_usb_device_path()
    print(f"LRCP Device ID: {device_id}")
    
    # The device path format is like: \\?\usb#vid_0c45&pid_6366#mi_00#{guid}
    # DirectShow uses device paths like: @device:pnp:\\\\?\USB#VID_0C45&PID_6366#...
    
    device_paths = [
        f"@device:pnp:\\\\?\\{device_id.replace('#', '\\#')}".upper(),
        f"@device:pnp:\\\\?\\{device_id}".upper(),
        device_id,
    ]
    
    for path in device_paths:
        print(f"Trying device path: {path}")
        try:
            cap = cv2.VideoCapture(path)
            if cap.isOpened():
                ret, frame = cap.read()
                cap.release()
                if ret:
                    print(f"  SUCCESS!")
                    return path
        except Exception as e:
            print(f"  Failed: {e}")
    return None

def try_video_device_index():
    """Try to find LRCP by checking all video devices"""
    print("\nScanning all video device indices...")
    for i in range(10):
        for backend in [cv2.CAP_DSHOW, cv2.CAP_MSMF, cv2.CAP_ANY]:
            try:
                cap = cv2.VideoCapture(i, backend)
                if cap.isOpened():
                    ret, frame = cap.read()
                    if ret:
                        brightness = np.mean(frame) if frame is not None else 0
                        print(f"  {backend}[{i}]: brightness={brightness:.1f}")
                    cap.release()
            except:
                pass

if __name__ == "__main__":
    print("=" * 50)
    print("LRCP H-720P Camera Access Test")
    print("=" * 50)
    
    device_path = get_usb_device_path()
    print(f"\nUSB Device: {device_path}")
    
    print("\nMethod 1: Try direct device path")
    result = try_direct_device_path()
    
    print("\nMethod 2: Try video device indices")
    try_video_device_index()
    
    print("\nDone.")
