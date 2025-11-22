"""
Alert system for sending notifications to stakeholders
"""
import os
import smtplib
import json
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timedelta
from models import db, Student, Contact, Alert, Attendance, Grade, Behavior, Assignment


class AlertSystem:
    """Handles alert generation and email notifications"""
    
    def __init__(self, app=None):
        self.app = app
        self.smtp_server = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
        self.smtp_port = int(os.getenv('SMTP_PORT', 587))
        self.smtp_username = os.getenv('SMTP_USERNAME', '')
        self.smtp_password = os.getenv('SMTP_PASSWORD', '')
        self.sender_email = os.getenv('SENDER_EMAIL', '')
        
        # Thresholds
        self.attendance_threshold = int(os.getenv('ATTENDANCE_THRESHOLD', 3))
        self.grade_threshold = float(os.getenv('GRADE_THRESHOLD', 70))
        self.behavior_threshold = int(os.getenv('BEHAVIOR_THRESHOLD', 2))
    
    def send_email(self, to_emails, subject, body):
        """Send email notification"""
        if not self.smtp_username or not self.smtp_password:
            print("Email configuration not set. Skipping email.")
            return False
        
        try:
            msg = MIMEMultipart('alternative')
            msg['From'] = self.sender_email
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = subject
            
            html_body = f"""
            <html>
              <body>
                <h2>Teacher Assistant Dashboard Alert</h2>
                {body}
                <hr>
                <p><small>This is an automated message from the Teacher Assistant Dashboard.</small></p>
              </body>
            </html>
            """
            
            msg.attach(MIMEText(html_body, 'html'))
            
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.smtp_username, self.smtp_password)
                server.send_message(msg)
            
            return True
        except Exception as e:
            print(f"Failed to send email: {e}")
            return False
    
    def check_attendance_alerts(self):
        """Check for attendance issues and send alerts"""
        alerts = []
        students = Student.query.all()
        
        for student in students:
            # Get absences in the last 30 days
            thirty_days_ago = datetime.utcnow().date() - timedelta(days=30)
            absences = Attendance.query.filter(
                Attendance.student_id == student.id,
                Attendance.date >= thirty_days_ago,
                Attendance.status.in_(['absent', 'tardy'])
            ).count()
            
            if absences >= self.attendance_threshold:
                severity = 'high' if absences >= self.attendance_threshold * 2 else 'medium'
                message = f"Student {student.first_name} {student.last_name} has {absences} absences/tardies in the last 30 days."
                alert = self.create_alert(student.id, 'attendance', severity, message)
                alerts.append(alert)
        
        return alerts
    
    def check_grade_alerts(self):
        """Check for low grades and send alerts"""
        alerts = []
        students = Student.query.all()
        
        for student in students:
            # Get recent grades (last 10)
            recent_grades = Grade.query.filter(
                Grade.student_id == student.id
            ).order_by(Grade.date.desc()).limit(10).all()
            
            if recent_grades:
                low_grades = [g for g in recent_grades if (g.score / g.max_score * 100) < self.grade_threshold]
                
                if len(low_grades) >= 3:  # 3 or more low grades
                    avg_percentage = sum(g.score / g.max_score * 100 for g in low_grades) / len(low_grades)
                    severity = 'high' if avg_percentage < 60 else 'medium'
                    message = f"Student {student.first_name} {student.last_name} has {len(low_grades)} grades below {self.grade_threshold}%. Average: {avg_percentage:.1f}%"
                    alert = self.create_alert(student.id, 'grade', severity, message)
                    alerts.append(alert)
        
        return alerts
    
    def check_behavior_alerts(self):
        """Check for behavior issues and send alerts"""
        alerts = []
        students = Student.query.all()
        
        for student in students:
            # Get behavior incidents in the last 14 days
            fourteen_days_ago = datetime.utcnow().date() - timedelta(days=14)
            incidents = Behavior.query.filter(
                Behavior.student_id == student.id,
                Behavior.date >= fourteen_days_ago
            ).all()
            
            if len(incidents) >= self.behavior_threshold:
                high_severity_count = sum(1 for i in incidents if i.severity == 'high')
                severity = 'high' if high_severity_count > 0 else 'medium'
                incident_types = ', '.join(set(i.incident_type for i in incidents))
                message = f"Student {student.first_name} {student.last_name} has {len(incidents)} behavior incidents in the last 14 days. Types: {incident_types}"
                alert = self.create_alert(student.id, 'behavior', severity, message)
                alerts.append(alert)
        
        return alerts
    
    def check_assignment_alerts(self):
        """Check for missing assignments and send alerts"""
        alerts = []
        students = Student.query.all()
        
        for student in students:
            # Get missing assignments
            missing = Assignment.query.filter(
                Assignment.student_id == student.id,
                Assignment.status.in_(['missing', 'late'])
            ).count()
            
            if missing >= 3:
                severity = 'high' if missing >= 5 else 'medium'
                message = f"Student {student.first_name} {student.last_name} has {missing} missing or late assignments."
                alert = self.create_alert(student.id, 'assignment', severity, message)
                alerts.append(alert)
        
        return alerts
    
    def create_alert(self, student_id, alert_type, severity, message):
        """Create and send an alert"""
        student = Student.query.get(student_id)
        if not student:
            return None
        
        # Get contacts who should receive alerts
        contacts = Contact.query.filter(
            Contact.student_id == student_id,
            Contact.receive_alerts == True,
            Contact.email.isnot(None)
        ).all()
        
        email_list = [c.email for c in contacts if c.email]
        
        if email_list:
            subject = f"Alert: {alert_type.title()} Issue for {student.first_name} {student.last_name}"
            body = f"<p><strong>Severity:</strong> {severity.upper()}</p><p>{message}</p>"
            body += f"<p><strong>Student:</strong> {student.first_name} {student.last_name} (ID: {student.student_id})</p>"
            
            if student.special_ed:
                body += "<p><strong>Note:</strong> This student has special education accommodations.</p>"
            
            # Send email
            self.send_email(email_list, subject, body)
        
        # Log the alert
        alert = Alert(
            student_id=student_id,
            alert_type=alert_type,
            severity=severity,
            message=message,
            sent_to=json.dumps(email_list)
        )
        db.session.add(alert)
        db.session.commit()
        
        return alert
    
    def run_all_checks(self):
        """Run all alert checks"""
        all_alerts = []
        all_alerts.extend(self.check_attendance_alerts())
        all_alerts.extend(self.check_grade_alerts())
        all_alerts.extend(self.check_behavior_alerts())
        all_alerts.extend(self.check_assignment_alerts())
        return all_alerts
