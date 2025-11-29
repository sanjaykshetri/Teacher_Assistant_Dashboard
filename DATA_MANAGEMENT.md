# 📚 Data Management Guide

## Table of Contents
1. [Overview](#overview)
2. [Data Security & Privacy](#data-security--privacy)
3. [Working with Data Files](#working-with-data-files)
4. [Excel Templates](#excel-templates)
5. [Data Validation](#data-validation)
6. [Best Practices](#best-practices)
7. [Troubleshooting](#troubleshooting)

---

## Overview

Your Teacher Assistant Dashboard uses **CSV files** to store all student data. These files are located in the `data/` folder and include:

- **`students.csv`** - Student information and parent contacts
- **`grades.csv`** - Assignment scores and grades
- **`attendance.csv`** - Daily attendance records
- **`behavior.csv`** - Behavior incidents (positive and negative)

---

## Data Security & Privacy

### ⚠️ CRITICAL: Protecting Student Privacy

**Student data is highly sensitive and must be protected!**

### Current Setup
✅ Your `.gitignore` file is configured to:
- Keep sample data in the repo (for development/testing)
- Exclude real student data from version control
- Protect Excel files with actual student information

### Recommended Approach

**Option 1: Private Repository (Recommended)**
```bash
# Make your repository private on GitHub:
# 1. Go to repository Settings
# 2. Scroll to "Danger Zone"
# 3. Click "Change visibility" → "Make private"
```

**Option 2: Local Data Only**
Keep real student data in a separate folder that's never committed:
```bash
# Create a 'real' data folder (already in .gitignore)
mkdir data/real
# Move your actual student files here
mv data/students.csv data/real/students.csv
# Modify app.py to load from data/real/ instead
```

**Option 3: Encrypted Storage**
For maximum security, use encrypted files or a password-protected database.

---

## Working with Data Files

### Method 1: Direct CSV Editing (Quick Updates)

**Best for:** Adding a single attendance record or grade

1. Open the CSV file in a text editor (VS Code, Notepad, etc.)
2. Add new rows following the exact format
3. Save the file
4. Refresh your dashboard

**Example - Adding attendance:**
```csv
student_id,date,status,notes
1,2025-11-29,present,
2,2025-11-29,absent,Sick
```

### Method 2: Excel Editing (Easier for Bulk Updates)

**Best for:** Multiple updates, easier viewing, less error-prone

#### Step-by-Step Process:

**Option A: Using Excel Templates (Recommended)**

1. **Open Template**
   ```
   Navigate to: data/templates/
   Open: students_template.xlsx (or grades, attendance, behavior)
   ```

2. **Enter Your Data**
   - Templates have formatted headers and helpful instructions
   - Each column shows what type of data to enter
   - Use the second row as a guide

3. **Export to CSV**
   - File → Save As
   - Format: CSV (Comma delimited) (*.csv)
   - Save to: `data/` folder
   - Name: `students.csv` (or appropriate name)

4. **Refresh Dashboard**
   - Reload your Streamlit app to see changes

**Option B: Edit Existing CSV in Excel**

1. **Open CSV in Excel**
   ```
   Right-click CSV → Open With → Excel
   OR
   Double-click (if Excel is default)
   ```

2. **Make Your Changes**
   - Be careful not to change column headers
   - Follow the data format guidelines below

3. **Save as CSV**
   - File → Save As → CSV (Comma delimited)
   - **Important:** Choose CSV, not Excel format!

4. **Refresh Dashboard**

---

## Excel Templates

Pre-formatted Excel templates are available in `data/templates/`:

### 📋 students_template.xlsx
| Column | Description | Example |
|--------|-------------|---------|
| student_id | Unique ID number | 1, 2, 3... |
| name | Full name | John Smith |
| email | Student email | john.smith@school.edu |
| parent_name | Parent/guardian name | Mary Smith |
| parent_email | Parent email | mary.smith@email.com |
| grade_level | Grade (9-12) | 10 |

### 📊 grades_template.xlsx
| Column | Description | Example |
|--------|-------------|---------|
| student_id | Student ID | 1 |
| assignment_name | Name of assignment | Quiz 1, Midterm Exam |
| assignment_type | Type | quiz, assignment, exam |
| score | Points earned | 85 |
| max_score | Points possible | 100 |
| date | Date (YYYY-MM-DD) | 2025-11-29 |

### 📅 attendance_template.xlsx
| Column | Description | Example |
|--------|-------------|---------|
| student_id | Student ID | 1 |
| date | Date (YYYY-MM-DD) | 2025-11-29 |
| status | Status | present, absent, tardy |
| notes | Optional notes | Sick, Late 10 minutes |

### 📝 behavior_template.xlsx
| Column | Description | Example |
|--------|-------------|---------|
| student_id | Student ID | 1 |
| date | Date (YYYY-MM-DD) | 2025-11-29 |
| incident_type | Type | positive, disruption |
| severity | Severity | low, medium, high |
| description | Brief description | Helped another student |

---

## Data Validation

### Running the Validator

Before using your dashboard, validate your data to catch errors:

```bash
python utils/data_validator.py
```

### What It Checks

✅ **Students File:**
- Valid email formats
- No duplicate student IDs
- All required fields filled
- Valid grade levels (9-12)

✅ **Grades File:**
- Student IDs exist in students file
- Scores don't exceed max scores
- No negative values
- Valid date formats

✅ **Attendance File:**
- Valid status values (present, absent, tardy)
- Student IDs exist
- No duplicate entries for same student/date
- Valid date formats

✅ **Behavior File:**
- Valid incident types and severities
- Student IDs exist
- Valid date formats
- Descriptions provided

### Understanding Validation Results

```
❌ ERRORS - Must be fixed before dashboard works correctly
⚠️  WARNINGS - Should be reviewed but won't break the dashboard
✅ SUCCESS - All data validated successfully
```

---

## Best Practices

### 🎯 Daily/Weekly Routine

**Daily:**
1. Take attendance → Update `attendance.csv` (or Excel template)
2. Record any behavior incidents → Update `behavior.csv`
3. Run data validator if making bulk changes

**After Grading:**
1. Open `grades_template.xlsx`
2. Enter all scores for the assignment
3. Save as `grades.csv`
4. Run validator: `python utils/data_validator.py`
5. Refresh dashboard

**Weekly:**
1. Review dashboard for at-risk students
2. Generate parent emails as needed
3. Backup your data files

### 💾 Backup Strategy

**Option 1: Manual Backups**
```bash
# Create a backup folder
mkdir -p backups/$(date +%Y-%m-%d)
# Copy all CSV files
cp data/*.csv backups/$(date +%Y-%m-%d)/
```

**Option 2: Git Commits (if private repo)**
```bash
git add data/*.csv
git commit -m "Update student data - Week of Nov 29"
git push
```

**Option 3: Cloud Sync**
- Use Dropbox, Google Drive, or OneDrive
- Keep your `data/` folder synced
- Enables access from multiple devices

### 📅 Data Format Guidelines

**Dates:** Always use `YYYY-MM-DD` format
- ✅ Correct: `2025-11-29`
- ❌ Wrong: `11/29/2025`, `Nov 29, 2025`

**Student IDs:** Use consistent numbering
- ✅ Correct: `1, 2, 3, 4...`
- ⚠️  Caution: Don't reuse IDs of former students

**Email Addresses:** Must be valid format
- ✅ Correct: `john.smith@school.edu`
- ❌ Wrong: `john.smith`, `john@school`

**Status Values:** Use exact values (case-sensitive)
- Attendance: `present`, `absent`, `tardy`, `excused`
- Behavior Type: `positive`, `disruption`
- Severity: `low`, `medium`, `high`

---

## Troubleshooting

### ❌ "File not found" Error
**Problem:** Dashboard can't find CSV files
**Solution:**
```bash
# Check files exist
ls data/
# Should show: attendance.csv, behavior.csv, grades.csv, students.csv
```

### ❌ "ParserError" or "CSV Error"
**Problem:** CSV file has formatting issues
**Solution:**
1. Open the problematic CSV in a text editor
2. Check for:
   - Missing commas
   - Extra commas
   - Unmatched quotes
3. Run validator: `python utils/data_validator.py`

### ⚠️ Student Not Appearing in Dashboard
**Problem:** Added student but they don't show up
**Checklist:**
1. Is student in `students.csv`?
2. Does student have a unique `student_id`?
3. Is the CSV format correct?
4. Did you refresh the dashboard (F5)?

### ⚠️ Email Not Generating
**Problem:** "Generate Email" button doesn't work
**Checklist:**
1. Does student have grades/attendance data?
2. Are there issues triggering the threshold?
3. Is parent email valid in `students.csv`?

### 🔄 Data Not Updating
**Problem:** Made changes but dashboard shows old data
**Solution:**
1. Hard refresh: Ctrl+F5 (Windows) or Cmd+Shift+R (Mac)
2. Restart Streamlit: Stop and run `streamlit run app.py` again
3. Check you saved the CSV file (not the Excel file)

---

## Quick Reference Commands

```bash
# Validate all data files
python utils/data_validator.py

# Start the dashboard
streamlit run app.py

# Create backup
cp data/*.csv backups/

# Check file formats
file data/*.csv

# View recent changes
git status
git diff data/

# Search for a student across all files
grep "John Smith" data/*.csv
```

---

## Need More Help?

### File Issues
- Check that files are in `data/` folder
- Ensure filenames match exactly: `students.csv`, not `Students.csv`
- Verify CSV format (comma-separated, no extra formatting)

### Data Issues
- Run the validator: `python utils/data_validator.py`
- Check date formats: YYYY-MM-DD
- Verify student IDs are consistent across files

### Dashboard Issues
- Restart Streamlit
- Check browser console for errors (F12)
- Verify all required CSV files exist

---

## Summary Workflow

```
┌─────────────────────────────────────────────────────┐
│ 1. Open Excel Template                              │
│    (data/templates/[type]_template.xlsx)            │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 2. Enter/Update Data                                │
│    (Use formatting guides and instructions)         │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 3. Save as CSV                                      │
│    (File → Save As → CSV format → data/ folder)    │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 4. Validate Data (Optional but Recommended)         │
│    (python utils/data_validator.py)                 │
└───────────────────┬─────────────────────────────────┘
                    │
┌───────────────────▼─────────────────────────────────┐
│ 5. Refresh Dashboard                                │
│    (F5 or restart Streamlit)                        │
└─────────────────────────────────────────────────────┘
```

---

**Remember:** Your student data is sensitive. Always keep it secure and backed up! 🔒
