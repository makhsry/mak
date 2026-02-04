import os
import time
import shutil
from datetime import datetime
import subprocess
import sys

class MotionDetectionScheduler:
    """
    Scheduler that runs existing Python scripts every 6 hours.
    
    Folder structure:
    root/
    ├── scripts/
    │   ├── camera_capture.py
    │   ├── motion_detector_advanced.py
    │   └── scheduler.py (this file)
    ├── tmp/                    (source images - cleaned after processing)
    └── reports/                (motion reports - preserved)
        └── motion_analysis/    (created by motion_detector_advanced.py)
    """
    
    def __init__(self, root_folder, interval_hours=6):
        """
        Initialize scheduler.
        
        Args:
            root_folder: Root folder (e.g., "C:\\Users\\MAK\\My Drive\\Temporary\\myroom")
            interval_hours: How often to run motion detection (default: 6)
        """
        self.root_folder = root_folder
        self.interval_hours = interval_hours
        
        # Define folder paths
        self.scripts_folder = os.path.join(root_folder, "scripts")
        self.tmp_folder = os.path.join(root_folder, "tmp")
        self.reports_folder = os.path.join(root_folder, "reports")
        
        # Define script paths
        self.motion_detector_script = os.path.join(self.scripts_folder, "motion_detector_advanced.py")
        
        # Create log folder
        self.log_folder = os.path.join(self.reports_folder, "logs")
        if not os.path.exists(self.log_folder):
            os.makedirs(self.log_folder)
        
        # Create log file
        log_filename = f"scheduler_{datetime.now().strftime('%Y%m%d_%H%M%S')}.log"
        self.log_path = os.path.join(self.log_folder, log_filename)
        
        # Verify folder structure
        self._verify_structure()
    
    def _verify_structure(self):
        """Verify required folders and scripts exist."""
        self.log("=" * 80)
        self.log("SCHEDULER INITIALIZATION")
        self.log("=" * 80)
        
        # Check folders
        required_folders = [
            (self.root_folder, "Root folder"),
            (self.scripts_folder, "Scripts folder"),
            (self.tmp_folder, "Tmp folder (source images)"),
            (self.reports_folder, "Reports folder")
        ]
        
        all_exist = True
        for folder, name in required_folders:
            if os.path.exists(folder):
                self.log(f"✓ {name}: {folder}")
            else:
                self.log(f"✗ {name} NOT FOUND: {folder}")
                all_exist = False
        
        # Check scripts
        if os.path.exists(self.motion_detector_script):
            self.log(f"✓ Motion detector script: {self.motion_detector_script}")
        else:
            self.log(f"✗ Motion detector script NOT FOUND: {self.motion_detector_script}")
            all_exist = False
        
        self.log("=" * 80)
        
        if not all_exist:
            self.log("\n⚠ ERROR: Required folders or scripts missing!")
            self.log("Please ensure folder structure matches:")
            self.log(f"  {self.root_folder}/")
            self.log(f"    scripts/")
            self.log(f"      motion_detector_advanced.py")
            self.log(f"      scheduler.py")
            self.log(f"    tmp/")
            self.log(f"    reports/")
            sys.exit(1)
    
    def log(self, message, also_print=True):
        """Write to log file and optionally print."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_message = f"[{timestamp}] {message}"
        
        if also_print:
            print(log_message)
        
        with open(self.log_path, 'a', encoding='utf-8') as f:
            f.write(log_message + "\n")
    
    def run_motion_detection(self):
        """Run motion detection and cleanup."""
        self.log("\n" + "=" * 80)
        self.log("MOTION DETECTION RUN STARTED")
        self.log("=" * 80)
        
        # Count images in tmp folder
        image_files = [f for f in os.listdir(self.tmp_folder) 
                      if f.endswith(('.jpg', '.jpeg', '.png'))]
        
        if len(image_files) < 2:
            self.log(f"⚠ Only {len(image_files)} image(s) in tmp folder")
            self.log("Need at least 2 images for motion detection. Skipping.")
            self.log("=" * 80)
            return
        
        self.log(f"📁 Found {len(image_files)} images to process")
        
        # Create timestamped report folder
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        run_report_folder = os.path.join(self.reports_folder, f"run_{timestamp}")
        os.makedirs(run_report_folder, exist_ok=True)
        
        self.log(f"📂 Report folder: {run_report_folder}")
        
        # Run motion_detector_advanced.py with custom output folder
        self.log(f"\n🔍 Running motion detector script...")
        try:
            # Create a temporary modified script that uses our output folder
            temp_script = os.path.join(self.scripts_folder, "temp_motion_detector.py")
            
            # Read original script
            with open(self.motion_detector_script, 'r', encoding='utf-8') as f:
                script_content = f.read()
            
            # Replace OUTPUT_FOLDER line
            script_content = script_content.replace(
                'OUTPUT_FOLDER = r"C:\\Users\\MAK\\My Drive\\Temporary\\myroom\\reports\\motion_analysis"',
                f'OUTPUT_FOLDER = r"{run_report_folder}"'
            )
            
            # Write temporary script
            with open(temp_script, 'w', encoding='utf-8') as f:
                f.write(script_content)
            
            # Run the temporary script
            result = subprocess.run(
                [sys.executable, temp_script],
                cwd=self.scripts_folder,
                capture_output=True,
                text=True,
                encoding='utf-8',
                errors='replace'
            )
            
            # Clean up temp script
            try:
                os.remove(temp_script)
            except:
                pass
            
            # Log output
            if result.stdout:
                self.log("\n--- Motion Detector Output ---")
                for line in result.stdout.split('\n'):
                    if line.strip():
                        self.log(line, also_print=False)
                self.log("--- End Output ---\n")
            
            if result.returncode != 0:
                self.log(f"⚠ Motion detector exited with code {result.returncode}")
                if result.stderr:
                    self.log(f"Error: {result.stderr}")
            else:
                self.log("✓ Motion detection completed successfully")
        
        except Exception as e:
            self.log(f"✗ Error running motion detector: {e}")
            import traceback
            self.log(traceback.format_exc())
            self.log("=" * 80)
            return
        
        # Clean up tmp folder
        self.log(f"\n🗑️  Cleaning up tmp folder...")
        deleted_count = 0
        failed_deletes = []
        
        for filename in image_files:
            try:
                os.remove(os.path.join(self.tmp_folder, filename))
                deleted_count += 1
            except Exception as e:
                failed_deletes.append((filename, str(e)))
        
        self.log(f"✓ Deleted {deleted_count}/{len(image_files)} images from tmp folder")
        
        if failed_deletes:
            self.log(f"⚠ Failed to delete {len(failed_deletes)} files:")
            for filename, error in failed_deletes:
                self.log(f"   {filename}: {error}", also_print=False)
        
        # Summary
        self.log("\n" + "=" * 80)
        self.log("RUN SUMMARY")
        self.log("=" * 80)
        self.log(f"✓ Images processed: {len(image_files)}")
        self.log(f"✓ Images deleted: {deleted_count}")
        self.log(f"✓ Reports saved to: {run_report_folder}")
        self.log("=" * 80)
    
    def run_continuous(self):
        """Run scheduler continuously."""
        self.log(f"\n⏰ Scheduler running every {self.interval_hours} hours")
        self.log(f"📂 Watching: {self.tmp_folder}")
        self.log(f"📝 Reports to: {self.reports_folder}")
        self.log(f"⌨️  Press Ctrl+C to stop\n")
        
        run_number = 0
        
        try:
            while True:
                run_number += 1
                self.log(f"\n{'='*80}")
                self.log(f"RUN #{run_number}")
                self.log(f"{'='*80}")
                
                # Run motion detection
                self.run_motion_detection()
                
                # Calculate next run time
                next_run = datetime.now().timestamp() + (self.interval_hours * 3600)
                next_run_str = datetime.fromtimestamp(next_run).strftime('%Y-%m-%d %H:%M:%S')
                
                self.log(f"\n⏰ Next run at: {next_run_str}")
                self.log(f"💤 Sleeping for {self.interval_hours} hours...\n")
                
                # Sleep
                time.sleep(self.interval_hours * 3600)
        
        except KeyboardInterrupt:
            self.log("\n\n⏹️  Scheduler stopped by user")
            self.log(f"Total runs completed: {run_number}")
            self.log("Goodbye!")
    
    def run_once(self):
        """Run motion detection once and exit."""
        self.log("\n🚀 Running single motion detection...")
        self.run_motion_detection()
        self.log("\n✓ Single run completed")


def main():
    """Main entry point."""
    # Configuration
    ROOT_FOLDER = r"C:\Users\MAK\My Drive\Temporary\myroom"
    INTERVAL_HOURS = 6
    
    # Parse command line argument
    run_mode = "continuous"  # default
    if len(sys.argv) > 1:
        if sys.argv[1] == "--once":
            run_mode = "once"
        elif sys.argv[1] == "--help":
            print("\nMotion Detection Scheduler")
            print("=" * 50)
            print("\nUsage:")
            print("  python scheduler.py           # Run continuously")
            print("  python scheduler.py --once    # Run once and exit")
            print("  python scheduler.py --help    # Show this help")
            print("\nFolder structure:")
            print(f"  {ROOT_FOLDER}/")
            print("    scripts/")
            print("      camera_capture.py")
            print("      motion_detector_advanced.py")
            print("      scheduler.py")
            print("    tmp/              (source images)")
            print("    reports/          (motion reports)")
            print("\n" + "=" * 50)
            return
    
    # Create scheduler
    scheduler = MotionDetectionScheduler(
        root_folder=ROOT_FOLDER,
        interval_hours=INTERVAL_HOURS
    )
    
    # Run based on mode
    if run_mode == "once":
        scheduler.run_once()
    else:
        scheduler.run_continuous()


if __name__ == "__main__":
    main()