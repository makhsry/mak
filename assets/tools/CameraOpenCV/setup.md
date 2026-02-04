# Setup Guide - Motion Detection System

## Folder Structure

```
C:\Users\MAK\My Drive\Temporary\myroom\
├── scripts\
│   ├── camera_capture.py
│   ├── motion_detector_advanced.py
│   └── scheduler.py
├── tmp\                                    (source images - auto-cleaned)
└── reports\                                (motion reports - preserved)
    ├── logs\
    │   └── scheduler_*.log
    ├── run_20260204_060000\                (First 6-hour run)
    │   ├── motion_report.json
    │   ├── motion_heatmap.jpg
    │   └── motion_capture_*.jpg            (only images with motion)
    ├── run_20260204_120000\                (Second 6-hour run)
    │   ├── motion_report.json
    │   ├── motion_heatmap.jpg
    │   └── motion_capture_*.jpg
    └── run_20260204_180000\                (Third 6-hour run)
        ├── motion_report.json
        ├── motion_heatmap.jpg
        └── motion_capture_*.jpg
```

---

## Installation Steps

### Step 1: Create Folder Structure
```powershell
# Open PowerShell and run:
cd "C:\Users\MAK\My Drive\Temporary\myroom"
New-Item -ItemType Directory -Path "scripts" -Force
New-Item -ItemType Directory -Path "tmp" -Force
New-Item -ItemType Directory -Path "reports" -Force
```

### Step 2: Place Files
Put these files in the `scripts\` folder:
- `camera_capture.py` 
- `motion_detector_advanced.py` 
- `scheduler.py` 

### Step 3: Install Python Packages
```powershell
pip install opencv-python numpy schedule
```

---

## Running the System

### Option 1: Using PowerShell Script (Recommended)

**Create `run_scheduler.ps1` in the scripts folder:**
```powershell
# Motion Detection Scheduler - PowerShell Runner
# Save as: run_scheduler.ps1

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Motion Detection Scheduler" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

# Change to scripts directory
$scriptDir = "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
Set-Location $scriptDir

Write-Host "📂 Working directory: $scriptDir" -ForegroundColor Green
Write-Host ""

# Run the scheduler
Write-Host "🚀 Starting scheduler..." -ForegroundColor Yellow
Write-Host "⌨️  Press Ctrl+C to stop" -ForegroundColor Yellow
Write-Host ""

python scheduler.py

Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "Scheduler stopped" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
```

**Then run:**
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
.\run_scheduler.ps1
```

### Option 2: Direct Python Command

**Terminal 1 - Camera Capture:**
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
python camera_capture.py
```

**Terminal 2 - Scheduler:**
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
python scheduler.py
```

---

## Scheduler Usage

### Run Continuously (Every 6 Hours)
```powershell
python scheduler.py
```

### Run Once (Test)
```powershell
python scheduler.py --once
```

### Show Help
```powershell
python scheduler.py --help
```

---

## How It Works

1. **Camera Capture** (`camera_capture.py`)
   - Runs continuously
   - Captures image every 5 seconds
   - Saves to `tmp\` folder

2. **Scheduler** (`scheduler.py`)
   - Runs every 6 hours
   - Calls `motion_detector_advanced.py`
   - Deletes processed images from `tmp\`
   - Logs everything to `reports\logs\`

3. **Motion Detection** (`motion_detector_advanced.py`)
   - Analyzes images in `tmp\`
   - Saves results to `reports\motion_analysis\`
   - Creates heatmap, JSON report, and annotated images

---

## Monitoring

### Check Logs
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports\logs"
dir
# Open latest log file
```

### Check Latest Report
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports"
dir | Sort-Object LastWriteTime -Descending | Select-Object -First 5
# Navigate to latest run_* folder
# Open motion_report.json or view motion images
```

### View Specific Run
```powershell
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports\run_20260204_120000"
dir
# View motion_report.json
# View motion_heatmap.jpg
# Check motion_capture_*.jpg images
```

---

## Troubleshooting

### Problem: Scheduler says "scripts not found"
**Solution:**
- Verify folder structure matches exactly
- Check that files are in `scripts\` folder
- Ensure paths in files are updated correctly

### Problem: No images in tmp folder
**Solution:**
- Make sure `camera_capture.py` is running
- Check that line 98 points to `tmp\` folder
- Verify camera is working

### Problem: Motion detection runs but no cleanup
**Solution:**
- Check scheduler logs in `reports\logs\`
- Verify Python has permission to delete files
- Look for error messages in log

---

## Configuration

### Change Processing Interval
Edit `scheduler.py` line 217:
```python
INTERVAL_HOURS = 6  # Change to 3, 12, 24, etc.
```

### Change Motion Sensitivity
Edit `motion_detector_advanced.py` line 244:
```python
sensitivity='medium'  # Options: 'low', 'medium', 'high'
```

---

## Quick Command Reference

```powershell
# Start camera capture
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
python camera_capture.py

# Start scheduler (continuous)
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
python scheduler.py

# Test run (once)
cd "C:\Users\MAK\My Drive\Temporary\myroom\scripts"
python scheduler.py --once

# View logs
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports\logs"
notepad scheduler_*.log

# View all runs
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports"
dir

# View latest report
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports"
dir | Sort-Object LastWriteTime -Descending | Select-Object -First 1
# Then cd into that run_* folder
```

---

## Stopping Everything

1. **Stop Camera:** Press `Ctrl+C` in camera terminal
2. **Stop Scheduler:** Press `Ctrl+C` in scheduler terminal

---

## Auto-Start with Windows (Optional)

**Create batch file: `start_all.bat`**
```batch
@echo off
cd /d "C:\Users\MAK\My Drive\Temporary\myroom\scripts"

start "Camera Capture" cmd /k python camera_capture.py
timeout /t 2
start "Motion Scheduler" cmd /k python scheduler.py

echo Both processes started in separate windows
```

Place in Startup folder:
1. Press `Win+R`
2. Type `shell:startup`
3. Place `start_all.bat` there

---

## Notes

- `tmp\` folder is automatically cleaned every 6 hours
- `reports\` folder keeps all motion history
- Logs are saved to `reports\logs\`
- Each run creates timestamped entries in logs
- Motion images are saved with green bounding boxes
