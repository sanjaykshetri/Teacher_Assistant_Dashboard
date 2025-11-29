# Data Folder Structure

This folder contains student data for the Teacher Assistant Dashboard.

## Folder Organization

```
data/
├── README.md                    # This file
├── students.csv                 # Main data files (currently sample data)
├── grades.csv
├── attendance.csv
├── behavior.csv
├── sample/                      # Sample/demo data (safe to commit to Git)
│   ├── students.csv
│   ├── grades.csv
│   ├── attendance.csv
│   └── behavior.csv
├── real/                        # Your actual student data (EXCLUDED from Git)
│   └── README.md                # Instructions for real data
└── templates/                   # Excel templates for easy data entry
    ├── students_template.xlsx
    ├── grades_template.xlsx
    ├── attendance_template.xlsx
    └── behavior_template.xlsx
```

## Quick Start

### For Development/Testing
Keep using the sample data files in the root `data/` folder or `data/sample/`.

### For Real Student Data

**Option 1: Use data/real/ folder (Recommended)**
1. Copy your CSV files to `data/real/`
2. Modify `app.py` to load from `data/real/` instead of `data/`
3. Files in `data/real/` are automatically excluded from Git

**Option 2: Make repository private**
1. Go to GitHub repository Settings
2. Change visibility to "Private"
3. Now you can safely use the root `data/` folder

**Option 3: Keep local only**
1. Never commit real student data
2. Keep CSVs only on your local machine
3. Use cloud storage (Dropbox, Google Drive) for backups

## Data Files Description

### students.csv
Core student information including:
- Student ID, name, email
- Parent/guardian name and email
- Grade level

### grades.csv
Assignment scores including:
- Assignment name and type
- Score and max possible score
- Date submitted

### attendance.csv
Daily attendance records:
- Date and status (present/absent/tardy)
- Optional notes

### behavior.csv
Behavior incidents (positive and negative):
- Incident type and severity
- Description of the incident

## Working with Data

See **[DATA_MANAGEMENT.md](../DATA_MANAGEMENT.md)** for detailed instructions on:
- How to edit data using Excel templates
- Data validation
- Best practices
- Troubleshooting

## Security Notes

🔒 **Student data is sensitive!** The `.gitignore` is configured to protect:
- `data/real/` folder
- All `.xlsx` files (except templates)
- Files ending in `_real.csv` or `_actual.csv`

Always verify your actual student data is NOT being committed to Git:
```bash
git status
# Should not show any files from data/real/
```
