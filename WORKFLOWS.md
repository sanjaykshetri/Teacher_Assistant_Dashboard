# 📋 Typical Workflows

## Scenario 1: Taking Daily Attendance

### Method A: Quick CSV Edit (1-2 minutes)
```bash
# Open attendance CSV
code data/attendance.csv

# Add today's attendance (copy and modify the last few lines):
# 1,2025-11-29,present,
# 2,2025-11-29,absent,Sick
# 3,2025-11-29,tardy,Late 10 min

# Save and refresh dashboard (F5)
```

### Method B: Excel Template (3-5 minutes)
```bash
# 1. Open template
open data/templates/attendance_template.xlsx

# 2. Fill in student IDs, today's date, and status
# 3. File → Save As → CSV → data/attendance.csv
# 4. Refresh dashboard
```

---

## Scenario 2: Entering Quiz Grades

### Best Method: Excel Template
```bash
# 1. Open grades template
open data/templates/grades_template.xlsx

# 2. For each student, enter:
#    - student_id: 1, 2, 3...
#    - assignment_name: "Quiz 4"
#    - assignment_type: "quiz"
#    - score: 85
#    - max_score: 100
#    - date: 2025-11-29

# 3. Convert to CSV (choose one):
#    A) File → Save As → CSV → data/grades.csv
#    B) python utils/excel_to_csv.py

# 4. Validate (recommended)
python utils/data_validator.py

# 5. Refresh dashboard to see new grades
```

---

## Scenario 3: Recording Behavior Incident

### Method A: Direct CSV Edit
```bash
# Open behavior.csv
code data/behavior.csv

# Add new row:
# 5,2025-11-29,disruption,medium,Talking during lecture

# Save and refresh
```

### Method B: Excel Template
```bash
# 1. Open template
open data/templates/behavior_template.xlsx

# 2. Add incident details
# 3. Save as CSV to data/behavior.csv
# 4. Refresh dashboard
```

---

## Scenario 4: Adding New Student

### Complete Workflow
```bash
# 1. Add to students.csv
# Open: data/templates/students_template.xlsx
# Enter: ID, name, email, parent info, grade level
# Save as: data/students.csv

# 2. Validate
python utils/data_validator.py

# 3. Add initial grades (if any)
# Use: data/templates/grades_template.xlsx

# 4. Add attendance records
# Use: data/templates/attendance_template.xlsx

# 5. Refresh dashboard
```

---

## Scenario 5: Weekly Grade Entry Session

### Efficient Bulk Entry
```bash
# Monday morning - enter all weekend grading at once

# 1. Open grades template
open data/templates/grades_template.xlsx

# 2. Enter all assignments graded over weekend:
#    Row 1: Student 1, Assignment 3, ...
#    Row 2: Student 2, Assignment 3, ...
#    Row 3: Student 3, Assignment 3, ...
#    ... (all students, one assignment)
#    
#    Row 31: Student 1, Quiz 2, ...
#    Row 32: Student 2, Quiz 2, ...
#    ... (all students, another assignment)

# 3. Convert and validate
python utils/excel_to_csv.py
python utils/data_validator.py

# 4. Generate parent emails for struggling students
# Use dashboard → Email Generator → Batch Email Generation
```

---

## Scenario 6: End of Grading Period Report

### Generate Emails for At-Risk Students
```bash
# 1. Ensure all data is up to date
python utils/data_validator.py

# 2. Start dashboard
streamlit run app.py

# 3. Go to "Dashboard" tab
#    - Review "Students Needing Attention"
#    - Check at-risk indicators

# 4. Go to "Batch Email Generation"
#    - Review list of students needing emails
#    - Click "Generate All Emails"
#    - Copy emails to send to parents

# 5. Document that emails were sent (optional)
#    Add note to behavior.csv or create separate log
```

---

## Scenario 7: Mid-Year Data Review

### Check Data Quality
```bash
# 1. Run comprehensive validation
python utils/data_validator.py

# 2. Review validation report
#    - Fix any errors (❌)
#    - Review warnings (⚠️)

# 3. Create backup
mkdir -p backups/2025-01-15
cp data/*.csv backups/2025-01-15/

# 4. Commit to Git (if using private repo)
git add data/*.csv
git commit -m "Mid-year data snapshot - January 2025"
git push
```

---

## Scenario 8: Preparing for Parent-Teacher Conferences

### Generate Individual Student Reports
```bash
# 1. Start dashboard
streamlit run app.py

# 2. For each student:
#    a. Go to "Student Records" tab
#    b. Select student from dropdown
#    c. Review all metrics:
#       - Current average grade
#       - Attendance rate
#       - Recent behavior incidents
#    d. Go to "Email Generator" tab
#    e. Generate parent email (use as talking points)
#    f. Print or save email content for reference

# 3. (Optional) Create conference notes file
#    Save generated emails to:
#    conference_notes/2025-01-15/
```

---

## Scenario 9: Start of New Semester

### Set Up Fresh Data Files
```bash
# 1. Archive previous semester data
mkdir -p archive/fall-2024
cp data/*.csv archive/fall-2024/

# 2. Keep students.csv (update grade levels if needed)
# Edit: data/students.csv
# Update: grade_level column (9→10, 10→11, etc.)

# 3. Clear or archive old grades/attendance
# Option A: Start fresh (empty except headers)
# Option B: Keep historical data

# 4. Add new students
# Use: data/templates/students_template.xlsx

# 5. Validate
python utils/data_validator.py

# 6. Git commit
git add data/*.csv
git commit -m "Start of Spring 2025 semester"
git push
```

---

## Scenario 10: Data Recovery (Oops, I deleted something!)

### Restore from Backup
```bash
# If using Git (private repo):
git log -- data/students.csv  # Find the commit
git checkout <commit-hash> -- data/students.csv

# If using local backups:
cp backups/2025-11-28/students.csv data/

# If using cloud sync (Dropbox/Google Drive):
# Use their version history feature to restore

# Always validate after restoration:
python utils/data_validator.py
```

---

## Time Estimates

| Task | Method | Time |
|------|--------|------|
| Daily attendance | CSV edit | 1-2 min |
| Daily attendance | Excel | 3-5 min |
| Grade one quiz (30 students) | Excel | 10-15 min |
| Add behavior incident | CSV edit | 1 min |
| Add new student | Excel + validate | 5 min |
| Weekly grade entry (50+ grades) | Excel + validate | 20-30 min |
| Generate emails (batch) | Dashboard | 2-3 min |
| Data validation | Script | 1 min |
| Backup data | Script | 1 min |

---

## Best Practices Reminder

1. **Validate regularly**: Run `python utils/data_validator.py` weekly
2. **Backup frequently**: Daily or weekly, depending on activity
3. **Use Excel for bulk**: Easier than CSV for multiple entries
4. **Use CSV for quick**: Single attendance or grade entry
5. **Check Git status**: Ensure sensitive data isn't being committed
6. **Refresh dashboard**: F5 after data changes
7. **Document workflows**: Add notes to this file for your specific needs

---

## Your Custom Workflows

Add your own workflows here as you discover what works best for you:

### Custom Workflow 1: [Your Title]
```
[Your steps here]
```

### Custom Workflow 2: [Your Title]
```
[Your steps here]
```
