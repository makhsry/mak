import cv2
import time
import os
from datetime import datetime
import sys

def capture_images(interval_seconds=5, save_folder="webcam_captures"):
    """
    Capture images from webcam at specified intervals.
    
    Args:
        interval_seconds: Time between captures (default: 60 seconds)
        save_folder: Folder to save captured images
    """
    # Create save folder if it doesn't exist
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
        print(f"Created folder: {save_folder}")
    
    capture_count = 0
    consecutive_failures = 0
    max_failures = 5
    
    def init_camera():
        """Initialize camera with proper settings"""
        print("Initializing camera...")
        cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)
        
        if not cap.isOpened():
            print("Trying alternative camera index...")
            cap = cv2.VideoCapture(0)
        
        if cap.isOpened():
            cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            cap.set(cv2.CAP_PROP_BUFFERSIZE, 1)  # Reduce buffer to avoid stale frames
            
            # Warm up the camera
            print("Warming up camera...")
            for i in range(10):
                ret, frame = cap.read()
                time.sleep(0.1)
            print("Camera ready!")
            return cap
        return None
    
    cap = init_camera()
    
    if cap is None:
        print("Error: Could not open webcam")
        print("\nTroubleshooting steps:")
        print("1. Check Windows Settings > Privacy & Security > Camera")
        print("2. Make sure 'Camera access' and 'Let apps access your camera' are ON")
        print("3. Close any other apps using the camera (Teams, Zoom, etc.)")
        print("4. Try running this script as Administrator")
        return
    
    print(f"Webcam opened successfully!")
    print(f"Capturing images every {interval_seconds} seconds")
    print("Press Ctrl+C to stop\n")
    
    try:
        while True:
            # Capture frame
            ret, frame = cap.read()
            
            if ret and frame is not None and frame.size > 0:
                # Reset failure counter on success
                consecutive_failures = 0
                
                # Generate filename with timestamp
                timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
                filename = os.path.join(save_folder, f"capture_{timestamp}.jpg")
                
                # Save image with high quality
                success = cv2.imwrite(filename, frame, [cv2.IMWRITE_JPEG_QUALITY, 95])
                
                if success:
                    capture_count += 1
                    file_size = os.path.getsize(filename) / 1024  # KB
                    print(f"[{capture_count}] Saved: capture_{timestamp}.jpg ({file_size:.1f} KB)")
                else:
                    print(f"Warning: Failed to save capture_{timestamp}.jpg")
                
                # Clear the frame from memory
                del frame
                
                # Wait for specified interval
                time.sleep(interval_seconds)
                
            else:
                consecutive_failures += 1
                print(f"Error: Failed to capture frame (failure #{consecutive_failures})")
                
                if consecutive_failures >= max_failures:
                    print(f"Too many consecutive failures ({max_failures}). Reinitializing camera...")
                    
                    # Release and reinitialize
                    cap.release()
                    time.sleep(2)
                    
                    cap = init_camera()
                    
                    if cap is None:
                        print("Error: Could not reinitialize webcam. Exiting.")
                        break
                    
                    consecutive_failures = 0
                else:
                    print("Retrying in 2 seconds...")
                    time.sleep(2)
                    # Clear buffer
                    for _ in range(5):
                        cap.grab()
                
    except KeyboardInterrupt:
        print("\n\nStopping capture...")
        print(f"Total images captured: {capture_count}")
    
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        print(f"Total images captured: {capture_count}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Release webcam
        if cap is not None:
            cap.release()
        cv2.destroyAllWindows()
        print("Webcam released. Goodbye!")

if __name__ == "__main__":
    # Capture every 5 seconds
    capture_images(interval_seconds=5, save_folder=r"C:\Users\MAK\My Drive\Temporary\myroom\tmp")