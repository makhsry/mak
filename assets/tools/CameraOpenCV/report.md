# Motion Detection Reports - Complete Guide

## 📂 Report Folder Structure

Each time the scheduler runs (every 6 hours), it creates a **timestamped folder**:

```
C:\Users\MAK\My Drive\Temporary\myroom\reports\
├── logs\
│   ├── scheduler_20260204_000000.log
│   ├── scheduler_20260204_060000.log
│   └── scheduler_20260204_120000.log
│
├── run_20260204_060000\          ← First run (6:00 AM)
│   ├── motion_report.json
│   ├── motion_heatmap.jpg
│   ├── motion_capture_20260204_060125.jpg
│   ├── motion_capture_20260204_060530.jpg
│   └── motion_capture_20260204_061245.jpg
│
├── run_20260204_120000\          ← Second run (12:00 PM)
│   ├── motion_report.json
│   ├── motion_heatmap.jpg
│   ├── motion_capture_20260204_120015.jpg
│   └── motion_capture_20260204_121530.jpg
│
└── run_20260204_180000\          ← Third run (6:00 PM)
    ├── motion_report.json
    ├── motion_heatmap.jpg
    └── motion_capture_20260204_180325.jpg
```

---

## 📄 Files in Each Run Folder

### 1. **motion_report.json**

**Purpose:** Complete data for all analyzed images

**Format:** JSON array with one object per image

**Example:**
```json
[
  {
    "filename": "capture_20260204_060005.jpg",
    "index": 0,
    "motion_detected": false,
    "motion_level": "NONE",
    "num_motion_areas": 0,
    "motion_percentage": 0.0,
    "motion_pixels": 0
  },
  {
    "filename": "capture_20260204_060010.jpg",
    "index": 1,
    "motion_detected": true,
    "motion_level": "LOW",
    "num_motion_areas": 1,
    "motion_percentage": 0.87,
    "motion_pixels": 2688
  },
  {
    "filename": "capture_20260204_060015.jpg",
    "index": 2,
    "motion_detected": true,
    "motion_level": "MEDIUM",
    "num_motion_areas": 3,
    "motion_percentage": 3.42,
    "motion_pixels": 10560
  },
  {
    "filename": "capture_20260204_060020.jpg",
    "index": 3,
    "motion_detected": true,
    "motion_level": "HIGH",
    "num_motion_areas": 5,
    "motion_percentage": 8.15,
    "motion_pixels": 25152
  }
]
```

**Fields Explanation:**
- `filename`: Original capture filename
- `index`: Sequential number (0, 1, 2, ...)
- `motion_detected`: true/false
- `motion_level`: "NONE", "LOW", "MEDIUM", or "HIGH"
- `num_motion_areas`: Number of separate motion regions detected
- `motion_percentage`: Percentage of frame with motion (0-100)
- `motion_pixels`: Total number of pixels that changed

**Motion Level Thresholds:**
- **NONE:** No motion detected
- **LOW:** < 1% of frame
- **MEDIUM:** 1% - 5% of frame
- **HIGH:** > 5% of frame

---

### 2. **motion_capture_YYYYMMDD_HHMMSS.jpg**

**Purpose:** Visual proof of motion with annotations

**Naming:** Uses original capture timestamp

**Features:**
- Green bounding boxes around detected motion areas
- Area size in pixels labeled on each box
- Red text overlay with:
  - Motion level (LOW/MEDIUM/HIGH)
  - Percentage of frame with motion
  - Number of motion areas
  - Original capture timestamp

**Example filenames:**
- `motion_capture_20260204_060125.jpg`
- `motion_capture_20260204_061530.jpg`
- `motion_capture_20260204_063445.jpg`

**Important:** Only images **WITH MOTION** are saved. Images with no motion are not saved (to save disk space).

---

### 3. **motion_heatmap.jpg**

**Purpose:** Cumulative visualization of motion hotspots

**Content:** Color-coded map showing where motion occurred most frequently during the 6-hour period

**Color Scale:**
- **Blue:** No motion / minimal activity
- **Green-Yellow:** Moderate activity
- **Orange-Red:** High activity / motion hotspot

**Use Cases:**
- Identify high-traffic areas in room
- See patterns of movement
- Detect if motion is concentrated in one area or spread out

---

## 📊 Understanding the Data

### Example Scenario: 6-Hour Period (6 AM - 12 PM)

**Camera captures:** Every 5 seconds = 4,320 images

**Motion detected in:** 127 images

**Report shows:**
```json
// Image with no motion (not saved as JPG)
{
  "filename": "capture_20260204_080015.jpg",
  "motion_detected": false,
  "motion_level": "NONE",
  "num_motion_areas": 0,
  "motion_percentage": 0.0
}

// Image with motion (saved as JPG)
{
  "filename": "capture_20260204_080125.jpg",
  "motion_detected": true,
  "motion_level": "MEDIUM",
  "num_motion_areas": 2,
  "motion_percentage": 2.34,
  "motion_pixels": 7228
}
```

**Files in folder:**
- `motion_report.json` → 4,320 entries (all images analyzed)
- `motion_capture_*.jpg` → 127 files (only images with motion)
- `motion_heatmap.jpg` → 1 file (cumulative visualization)

---

## 🔍 How to Analyze Reports

### Method 1: Quick Visual Check

1. Open the `run_YYYYMMDD_HHMMSS` folder
2. Look at `motion_capture_*.jpg` images
3. Check how many motion images exist
4. View `motion_heatmap.jpg` for overall pattern

### Method 2: JSON Analysis (Python)

```python
import json
from pathlib import Path

# Load report
report_path = r"C:\Users\MAK\My Drive\Temporary\myroom\reports\run_20260204_120000\motion_report.json"
with open(report_path) as f:
    data = json.load(f)

# Count motion detections
motion_count = sum(1 for item in data if item['motion_detected'])
total_count = len(data)

print(f"Motion detected in {motion_count}/{total_count} images")
print(f"Motion rate: {motion_count/total_count*100:.1f}%")

# Find peak motion
peak = max(data, key=lambda x: x['motion_percentage'])
print(f"\nPeak motion: {peak['motion_percentage']:.2f}%")
print(f"At: {peak['filename']}")

# List all high-motion events
high_motion = [item for item in data if item['motion_level'] == 'HIGH']
print(f"\nHigh motion events: {len(high_motion)}")
for item in high_motion:
    print(f"  {item['filename']}: {item['motion_percentage']:.2f}%")
```

### Method 3: PowerShell Quick Stats

```powershell
# Navigate to reports folder
cd "C:\Users\MAK\My Drive\Temporary\myroom\reports"

# Count runs
(Get-ChildItem -Directory -Filter "run_*").Count

# Count motion images in latest run
$latest = Get-ChildItem -Directory -Filter "run_*" | Sort-Object Name -Descending | Select-Object -First 1
(Get-ChildItem -Path $latest.FullName -Filter "motion_capture_*.jpg").Count

# List all runs
Get-ChildItem -Directory -Filter "run_*" | Sort-Object Name | Format-Table Name, LastWriteTime
```

---

## 📈 Interpreting Motion Levels

### LOW Motion (< 1% of frame)
**Examples:**
- Small object moving (pet, curtain flutter)
- Person passing by edge of frame
- Lighting changes (clouds, shadows)

**Action:** Usually safe to ignore unless investigating specific timing

### MEDIUM Motion (1-5% of frame)
**Examples:**
- Person walking through middle of frame
- Multiple small movements
- Object being moved

**Action:** Worth reviewing if checking for activity

### HIGH Motion (> 5% of frame)
**Examples:**
- Person in frame for extended time
- Multiple people
- Major scene changes

**Action:** Definitely review - significant activity occurred

---

## 🗂️ Report Retention

### What Gets Saved Forever
✅ All `run_*` folders with:
- `motion_report.json` (complete data)
- `motion_heatmap.jpg` (visual summary)
- `motion_capture_*.jpg` (proof images)

✅ All scheduler logs in `logs/`

### What Gets Deleted
❌ Original captures in `tmp/` folder (cleaned after each run)

### Storage Estimates (6-hour period)

**Source images (deleted):**
- 4,320 images × ~50 KB = ~216 MB (deleted every 6 hours)

**Reports (kept):**
- `motion_report.json`: ~200 KB
- `motion_heatmap.jpg`: ~200 KB
- Motion images: varies
  - 0% motion rate: ~400 KB per run
  - 5% motion rate: ~11 MB per run
  - 20% motion rate: ~44 MB per run

**Daily storage (4 runs):**
- Low activity: ~2 MB/day
- Normal activity: ~45 MB/day
- High activity: ~180 MB/day

---

## 🔧 Customizing Reports

### Change Motion Sensitivity

Edit `motion_detector_advanced.py` line 244:

```python
sensitivity='medium'  # Options: 'low', 'medium', 'high'
```

**Effect on reports:**
- **low:** Fewer motion detections, fewer saved images
- **high:** More motion detections, more saved images

### Disable Heatmap (Save Space)

Edit `motion_detector_advanced.py` line 245:

```python
save_heatmap=False  # Set to False
```

---

## 📋 Common Questions

### Q: Why are some captures missing from motion images?
**A:** Only images WITH MOTION are saved as JPG files. All images are analyzed and included in `motion_report.json`, but images without motion are not saved as separate files.

### Q: Can I see the original unmodified images?
**A:** No, original captures are deleted after processing. Only annotated motion images are kept. If you need originals, modify the scheduler to skip the cleanup step.

### Q: How do I find when motion occurred?
**A:** Check timestamps in filenames: `motion_capture_20260204_143025.jpg` = Feb 4, 2026 at 14:30:25 (2:30:25 PM)

### Q: Can I get a summary report instead of JSON?
**A:** The motion detector currently only creates JSON. You can add a summary by modifying the script or creating a post-processing script.

### Q: How long should I keep reports?
**A:** Depends on your needs:
- Security monitoring: Keep 30-90 days
- Pattern analysis: Keep 1-2 weeks
- Casual use: Keep 3-7 days

---

## 🚀 Advanced: Automated Report Analysis Script

Save this as `analyze_run.py` in the `scripts/` folder:

```python
import json
import sys
from pathlib import Path

def analyze_run(run_folder):
    """Analyze a single run and print summary."""
    run_path = Path(run_folder)
    report_path = run_path / "motion_report.json"
    
    if not report_path.exists():
        print(f"Error: Report not found in {run_folder}")
        return
    
    with open(report_path) as f:
        data = json.load(f)
    
    # Calculate statistics
    total = len(data)
    motion_items = [d for d in data if d['motion_detected']]
    motion_count = len(motion_items)
    
    if motion_count == 0:
        print(f"\n=== {run_path.name} ===")
        print(f"No motion detected in {total} images")
        return
    
    # Motion statistics
    avg_motion = sum(d['motion_percentage'] for d in motion_items) / motion_count
    peak = max(motion_items, key=lambda x: x['motion_percentage'])
    
    levels = {
        'LOW': len([d for d in motion_items if d['motion_level'] == 'LOW']),
        'MEDIUM': len([d for d in motion_items if d['motion_level'] == 'MEDIUM']),
        'HIGH': len([d for d in motion_items if d['motion_level'] == 'HIGH'])
    }
    
    # Print summary
    print(f"\n=== {run_path.name} ===")
    print(f"Total images analyzed: {total}")
    print(f"Motion detected: {motion_count} ({motion_count/total*100:.1f}%)")
    print(f"\nMotion levels:")
    print(f"  LOW:    {levels['LOW']:4d} ({levels['LOW']/motion_count*100:.1f}%)")
    print(f"  MEDIUM: {levels['MEDIUM']:4d} ({levels['MEDIUM']/motion_count*100:.1f}%)")
    print(f"  HIGH:   {levels['HIGH']:4d} ({levels['HIGH']/motion_count*100:.1f}%)")
    print(f"\nAverage motion: {avg_motion:.2f}%")
    print(f"Peak motion: {peak['motion_percentage']:.2f}% at {peak['filename']}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python analyze_run.py <run_folder>")
        print("Example: python analyze_run.py \"C:\\...\\reports\\run_20260204_120000\"")
    else:
        analyze_run(sys.argv[1])
```

**Usage:**
```powershell
python analyze_run.py "C:\Users\MAK\My Drive\Temporary\myroom\reports\run_20260204_120000"
```

---

## 📞 Quick Reference

| File | Purpose | Preserved? |
|------|---------|-----------|
| `motion_report.json` | Complete data for all images | ✅ Forever |
| `motion_heatmap.jpg` | Visual heat map | ✅ Forever |
| `motion_capture_*.jpg` | Annotated motion images | ✅ Forever |
| Scheduler logs | Run history and errors | ✅ Forever |
| Original captures in `tmp/` | Source images | ❌ Deleted after processing |
