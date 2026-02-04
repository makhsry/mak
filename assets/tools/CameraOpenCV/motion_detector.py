import cv2
import os
import numpy as np
from datetime import datetime

def detect_motion_in_images(image_folder, output_folder="motion_detected", 
                            motion_threshold=25, min_contour_area=500,
                            show_preview=False):
    """
    Analyze saved images for motion detection.
    
    Args:
        image_folder: Folder containing captured images
        output_folder: Folder to save images with detected motion
        motion_threshold: Sensitivity (lower = more sensitive, default: 25)
        min_contour_area: Minimum size of motion to detect in pixels (default: 500)
        show_preview: Whether to display images during processing
    
    Returns:
        List of images with detected motion
    """
    
    # Create output folder if it doesn't exist
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
        print(f"Created folder: {output_folder}")
    
    # Get all jpg files sorted by name (which includes timestamp)
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith('.jpg')])
    
    if len(image_files) < 2:
        print("Error: Need at least 2 images to detect motion")
        return []
    
    print(f"Found {len(image_files)} images")
    print(f"Motion threshold: {motion_threshold}")
    print(f"Minimum contour area: {min_contour_area} pixels")
    print("-" * 60)
    
    motion_detected_images = []
    previous_gray = None
    
    for i, filename in enumerate(image_files):
        filepath = os.path.join(image_folder, filename)
        
        # Read current image
        current_frame = cv2.imread(filepath)
        if current_frame is None:
            print(f"Warning: Could not read {filename}")
            continue
        
        # Convert to grayscale
        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        
        # Apply Gaussian blur to reduce noise
        current_gray = cv2.GaussianBlur(current_gray, (21, 21), 0)
        
        # Skip first image (no previous frame to compare)
        if previous_gray is None:
            previous_gray = current_gray
            print(f"[{i+1}/{len(image_files)}] {filename} - BASELINE (first image)")
            continue
        
        # Calculate absolute difference between current and previous frame
        frame_delta = cv2.absdiff(previous_gray, current_gray)
        
        # Threshold the difference
        thresh = cv2.threshold(frame_delta, motion_threshold, 255, cv2.THRESH_BINARY)[1]
        
        # Dilate to fill in holes
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        # Filter contours by area
        motion_contours = [c for c in contours if cv2.contourArea(c) >= min_contour_area]
        
        if len(motion_contours) > 0:
            # Motion detected!
            total_motion_area = sum(cv2.contourArea(c) for c in motion_contours)
            motion_percentage = (total_motion_area / (current_frame.shape[0] * current_frame.shape[1])) * 100
            
            # Draw rectangles around motion areas
            output_frame = current_frame.copy()
            for contour in motion_contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
            
            # Add text overlay
            text = f"MOTION DETECTED - {len(motion_contours)} area(s) - {motion_percentage:.2f}% of frame"
            cv2.putText(output_frame, text, (10, 30), 
                       cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 255), 2)
            cv2.putText(output_frame, filename, (10, 60),
                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 1)
            
            # Save annotated image
            output_path = os.path.join(output_folder, f"motion_{filename}")
            cv2.imwrite(output_path, output_frame)
            
            motion_detected_images.append({
                'filename': filename,
                'num_areas': len(motion_contours),
                'motion_percentage': motion_percentage,
                'total_area': total_motion_area
            })
            
            print(f"[{i+1}/{len(image_files)}] {filename} - ✓ MOTION: {len(motion_contours)} area(s), {motion_percentage:.2f}% of frame")
            
            if show_preview:
                # Show comparison
                cv2.imshow("Motion Detection", output_frame)
                cv2.imshow("Difference", thresh)
                cv2.waitKey(500)
        else:
            print(f"[{i+1}/{len(image_files)}] {filename} - No motion")
        
        # Update previous frame
        previous_gray = current_gray
    
    if show_preview:
        cv2.destroyAllWindows()
    
    print("-" * 60)
    print(f"\nSummary:")
    print(f"Total images analyzed: {len(image_files)}")
    print(f"Images with motion: {len(motion_detected_images)}")
    print(f"Images without motion: {len(image_files) - len(motion_detected_images) - 1}")
    
    if motion_detected_images:
        print(f"\nMotion detected in:")
        for item in motion_detected_images:
            print(f"  - {item['filename']}: {item['num_areas']} area(s), {item['motion_percentage']:.2f}% motion")
    
    return motion_detected_images


def create_motion_summary_video(image_folder, motion_data, output_video="motion_summary.mp4", fps=2):
    """
    Create a video showing only images with detected motion.
    
    Args:
        image_folder: Folder containing original images
        motion_data: List of motion detection results
        output_video: Output video filename
        fps: Frames per second for output video
    """
    if not motion_data:
        print("No motion detected - cannot create video")
        return
    
    print(f"\nCreating motion summary video...")
    
    # Read first image to get dimensions
    first_image = cv2.imread(os.path.join(image_folder, motion_data[0]['filename']))
    height, width = first_image.shape[:2]
    
    # Initialize video writer
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_video, fourcc, fps, (width, height))
    
    for item in motion_data:
        filepath = os.path.join(image_folder, item['filename'])
        frame = cv2.imread(filepath)
        if frame is not None:
            # Add timestamp and motion info
            text = f"{item['filename']} - {item['motion_percentage']:.1f}% motion"
            cv2.putText(frame, text, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 
                       0.7, (0, 255, 0), 2)
            out.write(frame)
    
    out.release()
    print(f"Video saved: {output_video}")


if __name__ == "__main__":
    # Configuration
    IMAGE_FOLDER = r"C:\Users\MAK\My Drive\Temporary\myroom"
    OUTPUT_FOLDER = r"C:\Users\MAK\My Drive\Temporary\myroom\motion_detected"
    
    # Adjust these parameters for sensitivity:
    # - Lower motion_threshold = more sensitive (10-50 typical range)
    # - Lower min_contour_area = detect smaller movements (100-2000 typical range)
    
    motion_data = detect_motion_in_images(
        image_folder=IMAGE_FOLDER,
        output_folder=OUTPUT_FOLDER,
        motion_threshold=25,        # Adjust sensitivity
        min_contour_area=500,       # Minimum motion size
        show_preview=False          # Set to True to see real-time analysis
    )
    
    # Optional: Create a video summary of motion events
    if motion_data:
        create_motion_summary_video(
            image_folder=IMAGE_FOLDER,
            motion_data=motion_data,
            output_video=os.path.join(OUTPUT_FOLDER, "motion_summary.mp4"),
            fps=2
        )
