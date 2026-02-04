# -*- coding: utf-8 -*-

import cv2
import os
import sys
import numpy as np
from datetime import datetime
import json

# Fix Windows console encoding
if sys.platform == 'win32':
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except:
        pass

def advanced_motion_detection(image_folder, output_folder="motion_analysis",
                              sensitivity="medium", save_heatmap=True):
    """
    Advanced motion detection with multiple algorithms and detailed analysis.
    
    Args:
        image_folder: Folder containing captured images
        output_folder: Folder to save analysis results
        sensitivity: 'low', 'medium', or 'high'
        save_heatmap: Whether to save motion heatmaps
    """
    
    # Sensitivity presets
    sensitivity_settings = {
        'low': {'threshold': 40, 'min_area': 1000},
        'medium': {'threshold': 25, 'min_area': 500},
        'high': {'threshold': 15, 'min_area': 200}
    }
    
    settings = sensitivity_settings.get(sensitivity, sensitivity_settings['medium'])
    
    # Create output folder
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    
    # Get sorted image files
    image_files = sorted([f for f in os.listdir(image_folder) if f.endswith(('.jpg', '.jpeg', '.png'))])
    
    if len(image_files) < 2:
        print("Error: Need at least 2 images to detect motion")
        return []
    
    print(f"Advanced Motion Detection")
    print(f"=" * 70)
    print(f"Images to analyze: {len(image_files)}")
    print(f"Sensitivity: {sensitivity.upper()}")
    print(f"Threshold: {settings['threshold']}")
    print(f"Min area: {settings['min_area']} pixels")
    print("=" * 70)
    
    results = []
    motion_heatmap = None
    previous_gray = None
    
    for i, filename in enumerate(image_files):
        filepath = os.path.join(image_folder, filename)
        current_frame = cv2.imread(filepath)
        
        if current_frame is None:
            continue
        
        # Initialize heatmap on first frame
        if motion_heatmap is None:
            motion_heatmap = np.zeros(current_frame.shape[:2], dtype=np.float32)
        
        # Convert to grayscale and blur
        current_gray = cv2.cvtColor(current_frame, cv2.COLOR_BGR2GRAY)
        current_gray = cv2.GaussianBlur(current_gray, (21, 21), 0)
        
        if previous_gray is None:
            previous_gray = current_gray
            print(f"[{i+1:3d}/{len(image_files)}] {filename:40s} - BASELINE")
            continue
        
        # Calculate frame difference
        frame_delta = cv2.absdiff(previous_gray, current_gray)
        thresh = cv2.threshold(frame_delta, settings['threshold'], 255, cv2.THRESH_BINARY)[1]
        thresh = cv2.dilate(thresh, None, iterations=2)
        
        # Update motion heatmap
        motion_heatmap += (thresh / 255.0)
        
        # Find contours
        contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        motion_contours = [c for c in contours if cv2.contourArea(c) >= settings['min_area']]
        
        # Calculate motion metrics
        total_motion_pixels = np.sum(thresh > 0)
        total_pixels = thresh.shape[0] * thresh.shape[1]
        motion_percentage = (total_motion_pixels / total_pixels) * 100
        
        # Determine motion level
        if len(motion_contours) == 0:
            motion_level = "NONE"
            symbol = "[ ]"   # NONE // symbol = "○"
        elif motion_percentage < 1:
            motion_level = "LOW"
            symbol = "[●]"   # LOW // symbol = "●"
        elif motion_percentage < 5:
            motion_level = "MEDIUM"
            symbol = "[●●]"   # MEDIUM // symbol = "●●"
        else:
            motion_level = "HIGH"
            symbol = "[●●●]"   # HIGH // symbol = "●●●"
        
        result = {
            'filename': filename,
            'index': i,
            'motion_detected': len(motion_contours) > 0,
            'motion_level': motion_level,
            'num_motion_areas': len(motion_contours),
            'motion_percentage': motion_percentage,
            'motion_pixels': int(total_motion_pixels)
        }
        results.append(result)
        
        # Print status
        status = f"[{i+1:3d}/{len(image_files)}] {filename:40s} - {symbol} {motion_level:6s} "
        if motion_percentage > 0:
            status += f"({motion_percentage:5.2f}%, {len(motion_contours)} area(s))"
        print(status)
        
        # Save annotated image if motion detected
        if len(motion_contours) > 0:
            output_frame = current_frame.copy()
            
            # Draw bounding boxes
            for contour in motion_contours:
                (x, y, w, h) = cv2.boundingRect(contour)
                cv2.rectangle(output_frame, (x, y), (x + w, y + h), (0, 255, 0), 2)
                area = cv2.contourArea(contour)
                cv2.putText(output_frame, f"{int(area)}px", (x, y-5),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
            
            # Add info overlay
            info_text = [
                f"Motion: {motion_level} ({motion_percentage:.2f}%)",
                f"Areas: {len(motion_contours)}",
                f"Time: {filename.replace('capture_', '').replace('.jpg', '')}"
            ]
            
            for idx, text in enumerate(info_text):
                y_pos = 30 + (idx * 30)
                cv2.putText(output_frame, text, (10, y_pos),
                           cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
            
            # Save
            output_path = os.path.join(output_folder, f"motion_{filename}")
            cv2.imwrite(output_path, output_frame)
        
        previous_gray = current_gray
    
    # Create and save motion heatmap
    if save_heatmap and motion_heatmap is not None:
        # Normalize heatmap
        heatmap_normalized = cv2.normalize(motion_heatmap, None, 0, 255, cv2.NORM_MINMAX)
        heatmap_colored = cv2.applyColorMap(heatmap_normalized.astype(np.uint8), cv2.COLORMAP_JET)
        
        # Add legend
        cv2.putText(heatmap_colored, "Motion Heatmap - Cumulative Activity", (10, 30),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)
        cv2.putText(heatmap_colored, "Blue = No Motion, Red = Most Motion", (10, 60),
                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
        
        heatmap_path = os.path.join(output_folder, "motion_heatmap.jpg")
        cv2.imwrite(heatmap_path, heatmap_colored)
        print(f"\n✓ Motion heatmap saved: {heatmap_path}")
    
    # Save JSON report
    report_path = os.path.join(output_folder, "motion_report.json")
    with open(report_path, 'w') as f:
        json.dump(results, f, indent=2)
    print(f"✓ Motion report saved: {report_path}")
    
    # Print summary
    print("\n" + "=" * 70)
    print("SUMMARY")
    print("=" * 70)
    
    motion_images = [r for r in results if r['motion_detected']]
    no_motion_images = [r for r in results if not r['motion_detected']]
    
    print(f"Total images analyzed: {len(results)}")
    print(f"Images with motion:    {len(motion_images)} ({len(motion_images)/len(results)*100:.1f}%)")
    print(f"Images without motion: {len(no_motion_images)} ({len(no_motion_images)/len(results)*100:.1f}%)")
    
    if motion_images:
        print(f"\nMotion statistics:")
        avg_motion = np.mean([r['motion_percentage'] for r in motion_images])
        max_motion = max(motion_images, key=lambda x: x['motion_percentage'])
        print(f"  Average motion: {avg_motion:.2f}%")
        print(f"  Maximum motion: {max_motion['motion_percentage']:.2f}% in {max_motion['filename']}")
        
        # Motion timeline
        print(f"\nMotion timeline:")
        for r in motion_images[:10]:  # Show first 10
            print(f"  {r['filename']}: {r['motion_level']} ({r['motion_percentage']:.2f}%)")
        if len(motion_images) > 10:
            print(f"  ... and {len(motion_images) - 10} more")
    
    print("=" * 70)
    
    return results


if __name__ == "__main__":
    # Configuration
    IMAGE_FOLDER = r"C:\Users\MAK\My Drive\Temporary\myroom\tmp"
    OUTPUT_FOLDER = r"C:\Users\MAK\My Drive\Temporary\myroom\reports"
    
    # Run analysis
    # sensitivity options: 'low', 'medium', 'high'
    results = advanced_motion_detection(
        image_folder=IMAGE_FOLDER,
        output_folder=OUTPUT_FOLDER,
        sensitivity='medium',  # Adjust this
        save_heatmap=True
    )
