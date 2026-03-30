"""
Camera Capture Tool for Windows
Uses OpenCV to capture photos from available cameras
"""
import cv2
import os
import sys
from datetime import datetime

def list_cameras(max_check=5):
    """Check available cameras"""
    available = []
    for i in range(max_check):
        cap = cv2.VideoCapture(i, cv2.CAP_DSHOW)
        if cap is None or not cap.isOpened():
            cap.release()
            continue
        ret, frame = cap.read()
        if ret:
            available.append(i)
            print(f"  Camera {i}: OK")
        cap.release()
    return available

def capture_photo(camera_idx=0, output_dir=None):
    """Capture a photo from specified camera"""
    if output_dir is None:
        output_dir = os.path.dirname(os.path.abspath(__file__))
    
    cap = cv2.VideoCapture(camera_idx, cv2.CAP_DSHOW)
    if not cap.isOpened():
        print(f"Error: Cannot open camera {camera_idx}")
        return None
    
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
    
    # Capture from first available camera
    print(f"\nCapturing from camera {cameras[0]}...")
    result = capture_photo(cameras[0])
    
    if result:
        print(f"\nSuccess! Photo saved to:\n  {result}")
    else:
        print("\nCapture failed!")

if __name__ == "__main__":
    main()
