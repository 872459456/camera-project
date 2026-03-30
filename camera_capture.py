"""
Camera Capture Tool for Windows
Uses OpenCV to capture photos from available cameras

Tested cameras:
- Integrated IR Camera (1280x720 works)
- Integrated Camera (640x480 works)
- LRCP H-720P (not accessible via OpenCV)
"""
import cv2
import os
import sys
from datetime import datetime

def list_cameras(max_check=10):
    """Check available cameras with both DSHOW and MSMF backends"""
    available = []
    backends = [
        ('MSMF', cv2.CAP_MSMF),
        ('DSHOW', cv2.CAP_DSHOW),
    ]
    
    for backend_name, backend in backends:
        for i in range(max_check):
            cap = cv2.VideoCapture(i, backend)
            if cap.isOpened():
                ret, frame = cap.read()
                if ret:
                    brightness = 0
                    if frame is not None and frame.size > 0:
                        import numpy as np
                        brightness = np.mean(frame)
                    available.append({
                        'index': i,
                        'backend': backend_name,
                        'brightness': brightness,
                        'shape': frame.shape if frame is not None else None
                    })
                    print(f"  Camera {i} ({backend_name}): brightness={brightness:.1f}, shape={frame.shape}")
                cap.release()
    return available

def capture_photo(camera_idx=0, output_dir=None, resolution=(1280, 720)):
    """Capture a photo from specified camera with specified resolution"""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Try MSMF backend first (better for Windows)
    cap = cv2.VideoCapture(camera_idx, cv2.CAP_MSMF)
    if not cap.isOpened():
        # Fall back to DSHOW
        cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
    
    if not cap.isOpened():
        print(f"Error: Cannot open camera {camera_idx}")
        return None
    
    # Set resolution
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, resolution[0])
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, resolution[1])
    
    actual_width = cap.get(cv2.CAP_PROP_FRAME_WIDTH)
    actual_height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT)
    print(f"Camera resolution: {actual_width}x{actual_height}")
    
    ret, frame = cap.read()
    cap.release()
    
    if not ret:
        print(f"Error: Failed to capture from camera {camera_idx}")
        return None
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"photo_cam{camera_idx}_{timestamp}.jpg"
    filepath = os.path.join(output_dir, filename)
    
    cv2.imwrite(filepath, frame)
    print(f"Photo saved: {filename}")
    return filepath

def main():
    print("=" * 50)
    print("Camera Capture Tool for Windows")
    print("=" * 50)
    
    print("\nDetecting cameras...")
    cameras = list_cameras()
    
    if not cameras:
        print("No cameras found!")
        return
    
    print(f"\nFound {len(cameras)} camera(s)")
    
    # Use the first available camera
    camera = cameras[0]
    print(f"\nCapturing from camera {camera['index']} ({camera['backend']})...")
    result = capture_photo(camera['index'])
    
    if result:
        print(f"\nSuccess! Photo saved to:\n  {result}")
    else:
        print("\nCapture failed!")

if __name__ == "__main__":
    main()
