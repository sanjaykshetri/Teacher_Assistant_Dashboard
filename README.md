# Teacher Assistant Dashboard 📚

A comprehensive Streamlit dashboard designed to centralize and streamline various aspects of teaching responsibilities, including student record management and automated email generation.

## Features

### 📊 Dashboard Overview
- Real-time student performance metrics
- Class-wide statistics (average grades, attendance rates)
- At-risk student identification
- Color-coded performance indicators

### 📋 Student Records
- Detailed individual student profiles
- Grade tracking (assignments, quizzes, exams)
- Attendance monitoring
- Behavior incident logging
- Parent contact information

### ✉️ Email Generator
- Automated email generation based on student performance
- Personalized messages for different recipients:
  - **Parent Emails**: Concerns about grades, attendance, or behavior
  - **Student Emails**: Encouragement and performance feedback
  - **Admin Emails**: Critical cases requiring intervention
- Customizable thresholds for triggering communications

### 📬 Batch Email Generation
- Bulk email generation for all students requiring attention
- Summary of students needing communication
- One-click generation for multiple recipients

## Installation

1. Clone the repository:
```bash
git clone https://github.com/sanjaykshetri/Teacher_Assistant_Dashboard.git
cd Teacher_Assistant_Dashboard
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

## Usage

1. Start the Streamlit dashboard:
```bash
streamlit run app.py
```

2. The dashboard will open in your default web browser at `http://localhost:8501`

3. Use the sidebar to navigate between different sections:
   - **Dashboard**: View overall class performance
   - **Student Records**: Access detailed student information
   - **Email Generator**: Create individual student emails
   - **Batch Email Generation**: Generate multiple emails at once

## Data Management

### 📊 Data Structure

The application uses CSV files stored in the `data/` directory:

- **students.csv**: Student information and parent contacts
- **grades.csv**: Assignment scores and grades
- **attendance.csv**: Daily attendance records
- **behavior.csv**: Behavior incidents (positive and negative)

### 📝 Excel Templates

Pre-formatted Excel templates are available in `data/templates/` for easier data entry:
- Easy-to-use spreadsheet interface
- Formatted headers and helpful instructions
- Simply fill in data and convert to CSV

**Quick workflow:**
```bash
# 1. Edit Excel template (e.g., data/templates/grades_template.xlsx)
# 2. Convert to CSV
python utils/excel_to_csv.py
# 3. Validate data
python utils/data_validator.py
# 4. Refresh dashboard
```

### 🔒 Data Privacy & Security

**IMPORTANT:** Student data is sensitive and protected by `.gitignore`:
- Use `data/real/` folder for actual student data (excluded from Git)
- Current `data/` folder contains sample data only
- Consider making your repository private for added security

See **[DATA_MANAGEMENT.md](DATA_MANAGEMENT.md)** for complete instructions.

### ✅ Data Validation

Validate your data files before using the dashboard:
```bash
python utils/data_validator.py
```

This checks for:
- Invalid email formats
- Missing required fields
- Duplicate entries
- Incorrect date formats
- Invalid student IDs

## Customization

### Teacher Information
Update teacher name and email in the sidebar settings to personalize email signatures.

### Email Thresholds
Modify thresholds in `utils/email_generator.py`:
- `LOW_GRADE_THRESHOLD`: Default 70%
- `CRITICAL_GRADE_THRESHOLD`: Default 60%
- `LOW_ATTENDANCE_THRESHOLD`: Default 80%
- `CRITICAL_ATTENDANCE_THRESHOLD`: Default 70%
- `MULTIPLE_INCIDENTS_THRESHOLD`: Default 2

### Email Templates
Email templates can be customized in the `EmailGenerator` class methods:
- `generate_parent_email()`
- `generate_student_email()`
- `generate_admin_email()`

## Sample Data

The repository includes sample data for 10 students with various performance levels:
- High performers (90%+ average)
- Average performers (70-89%)
- At-risk students (below 70%)
- Students with attendance issues
- Students with behavior concerns

## Future Enhancements

Potential features for future versions:
- Integration with school email systems (SMTP)
- Export emails to PDF or text files
- Grade trend analysis and visualization
- Assignment deadline tracking
- Automated weekly/monthly reports
- Integration with Learning Management Systems (LMS)
- Mobile-responsive design improvements

## License

This project is licensed under the terms included in the LICENSE file.

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## Support

For questions or issues, please open an issue on the GitHub repository. 
