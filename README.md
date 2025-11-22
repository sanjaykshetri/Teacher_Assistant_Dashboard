# Teacher Assistant Dashboard 🎓

A comprehensive web-based dashboard system designed to help teachers manage and monitor all aspects of student data in one centralized location. The system tracks attendance, grades, assignments, behavioral incidents, and stakeholder contact information, with automated email alerts to keep parents, counselors, and administrators informed.

## Features

### Student Data Management
- **Student Profiles**: Store comprehensive student information including ID, grade level, special education status, and accommodations
- **Attendance Tracking**: Record daily attendance with statuses (present, absent, tardy, excused)
- **Grade Management**: Track grades across multiple subjects and assignments with automatic percentage calculations
- **Assignment Monitoring**: Monitor assignment submissions, due dates, and completion status
- **Behavior Tracking**: Document behavioral incidents with severity levels and actions taken

### Stakeholder Communication
- **Contact Management**: Store contact information for:
  - Parents/Guardians
  - School Counselors
  - Assistant Principals
  - Special Education Coordinators
- **Email Alerts**: Automated notifications sent to relevant stakeholders based on configurable thresholds

### Alert System
The system automatically monitors and sends alerts for:
- **Attendance Issues**: Alerts when absences/tardies exceed threshold (default: 3 in 30 days)
- **Low Grades**: Alerts when multiple grades fall below threshold (default: 70%)
- **Behavior Concerns**: Alerts when behavior incidents exceed threshold (default: 2 in 14 days)
- **Missing Assignments**: Alerts when missing/late assignments accumulate (default: 3+)

### Dashboard Features
- **Overview Summary**: Quick statistics on total students, active alerts, and severity breakdown
- **Interactive Tables**: View and filter data across all categories
- **Student Detail View**: Comprehensive view of individual student data
- **Real-time Updates**: Refresh data and run alert checks on demand

## Technology Stack

- **Backend**: Python Flask
- **Database**: SQLite with SQLAlchemy ORM
- **Frontend**: HTML, CSS, JavaScript (Vanilla)
- **Email**: SMTP for automated notifications

## Installation

### Prerequisites
- Python 3.8 or higher
- pip (Python package installer)

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/sanjaykshetri/Teacher_Assistant_Dashboard.git
   cd Teacher_Assistant_Dashboard
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   ```bash
   cp .env.example .env
   ```
   
   Edit `.env` and configure your settings:
   - Email settings (SMTP server, credentials)
   - Alert thresholds
   - Flask configuration

5. **Initialize the database**
   ```bash
   python app.py
   ```
   This will create the database and start the server.

6. **Load sample data** (optional, for testing)
   ```bash
   python sample_data.py
   ```

7. **Access the dashboard**
   Open your browser and navigate to:
   ```
   http://localhost:5000
   ```

## Configuration

### Email Setup
To enable automated email alerts, configure the following in your `.env` file:

```env
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
SMTP_USERNAME=your_email@gmail.com
SMTP_PASSWORD=your_app_password
SENDER_EMAIL=your_email@gmail.com
```

**Note for Gmail users**: You'll need to use an [App Password](https://support.google.com/accounts/answer/185833) instead of your regular password.

### Alert Thresholds
Customize alert sensitivity by adjusting these values in `.env`:

```env
ATTENDANCE_THRESHOLD=3      # Number of absences/tardies to trigger alert
GRADE_THRESHOLD=70          # Percentage below which to flag grades
BEHAVIOR_THRESHOLD=2        # Number of incidents to trigger alert
```

## Usage

### Adding Students
1. Click the "Add Student" button on the dashboard
2. Fill in student information (name, ID, grade level, special ed status, accommodations)
3. Submit the form

### Viewing Student Details
- Click the "View" button next to any student in the Students tab
- This opens a detailed view showing all data for that student including:
  - Student information
  - Contact list
  - Recent alerts
  - Attendance history
  - Grade history
  - Assignment status
  - Behavior incidents

### Running Alert Checks
- Click the "Run Alert Check" button to manually trigger the alert system
- The system will analyze all student data and send emails to stakeholders as needed
- Alerts are logged in the database and visible in the Alerts tab

### API Endpoints
The system provides a RESTful API for programmatic access:

- `GET /api/students` - List all students
- `POST /api/students` - Create a new student
- `GET /api/students/<id>/dashboard` - Get comprehensive student data
- `GET/POST /api/attendance` - Manage attendance records
- `GET/POST /api/grades` - Manage grades
- `GET/POST /api/assignments` - Manage assignments
- `GET/POST /api/behaviors` - Manage behavior incidents
- `GET/POST /api/contacts` - Manage contacts
- `GET /api/alerts` - View alerts
- `POST /api/alerts/check` - Trigger alert check
- `GET /api/dashboard/summary` - Get dashboard statistics

## Project Structure

```
Teacher_Assistant_Dashboard/
├── app.py                  # Main Flask application
├── models.py              # Database models
├── alert_system.py        # Alert checking and email logic
├── sample_data.py         # Script to generate sample data
├── requirements.txt       # Python dependencies
├── .env.example          # Example environment configuration
├── .gitignore            # Git ignore rules
├── README.md             # This file
└── static/               # Frontend files
    ├── index.html        # Main dashboard HTML
    ├── style.css         # Styling
    └── app.js            # Frontend JavaScript
```

## Development

### Database Models
- **Student**: Core student information
- **Attendance**: Daily attendance records
- **Grade**: Assignment grades and scores
- **Assignment**: Assignment tracking
- **Behavior**: Behavioral incident records
- **Contact**: Stakeholder contact information
- **Alert**: Alert history log

### Extending the System
To add new features:
1. Update database models in `models.py`
2. Add API endpoints in `app.py`
3. Update alert logic in `alert_system.py` if needed
4. Add frontend functionality in `static/app.js` and `static/index.html`

## Security Considerations

- Never commit `.env` file or expose sensitive credentials
- Use environment variables for all sensitive configuration
- Implement proper authentication if deploying to production
- Use HTTPS in production environments
- Regularly update dependencies for security patches

## License

This project is licensed under the terms specified in the LICENSE file.

## Support

For issues, questions, or contributions, please visit the GitHub repository:
https://github.com/sanjaykshetri/Teacher_Assistant_Dashboard

## Future Enhancements

Potential features for future development:
- User authentication and role-based access control
- Data export (PDF reports, CSV downloads)
- Advanced analytics and visualizations
- Mobile app version
- Integration with school information systems
- Automated schedule-based alert checks
- SMS notifications
- Document upload and management
- Parent portal for self-service access 
