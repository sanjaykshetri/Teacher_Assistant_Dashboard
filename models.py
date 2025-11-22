"""
Database models for Teacher Assistant Dashboard
"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Student(db.Model):
    """Student information model"""
    __tablename__ = 'students'
    
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(100), nullable=False)
    last_name = db.Column(db.String(100), nullable=False)
    student_id = db.Column(db.String(50), unique=True, nullable=False)
    grade_level = db.Column(db.Integer)
    special_ed = db.Column(db.Boolean, default=False)
    accommodations = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    # Relationships
    attendances = db.relationship('Attendance', backref='student', lazy=True, cascade='all, delete-orphan')
    grades = db.relationship('Grade', backref='student', lazy=True, cascade='all, delete-orphan')
    assignments = db.relationship('Assignment', backref='student', lazy=True, cascade='all, delete-orphan')
    behaviors = db.relationship('Behavior', backref='student', lazy=True, cascade='all, delete-orphan')
    contacts = db.relationship('Contact', backref='student', lazy=True, cascade='all, delete-orphan')
    
    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'student_id': self.student_id,
            'grade_level': self.grade_level,
            'special_ed': self.special_ed,
            'accommodations': self.accommodations,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Attendance(db.Model):
    """Attendance records model"""
    __tablename__ = 'attendance'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    status = db.Column(db.String(20), nullable=False)  # present, absent, tardy, excused
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'date': self.date.isoformat() if self.date else None,
            'status': self.status,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Grade(db.Model):
    """Grades model"""
    __tablename__ = 'grades'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    subject = db.Column(db.String(100), nullable=False)
    assignment_name = db.Column(db.String(200), nullable=False)
    score = db.Column(db.Float, nullable=False)
    max_score = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)
    notes = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'subject': self.subject,
            'assignment_name': self.assignment_name,
            'score': self.score,
            'max_score': self.max_score,
            'percentage': round((self.score / self.max_score * 100), 2) if self.max_score > 0 else 0,
            'date': self.date.isoformat() if self.date else None,
            'notes': self.notes,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Assignment(db.Model):
    """Assignments model"""
    __tablename__ = 'assignments'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    title = db.Column(db.String(200), nullable=False)
    description = db.Column(db.Text)
    due_date = db.Column(db.Date, nullable=False)
    submitted = db.Column(db.Boolean, default=False)
    submission_date = db.Column(db.Date)
    status = db.Column(db.String(20), nullable=False)  # pending, submitted, late, missing
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'title': self.title,
            'description': self.description,
            'due_date': self.due_date.isoformat() if self.due_date else None,
            'submitted': self.submitted,
            'submission_date': self.submission_date.isoformat() if self.submission_date else None,
            'status': self.status,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Behavior(db.Model):
    """Behavior incidents model"""
    __tablename__ = 'behaviors'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    date = db.Column(db.Date, nullable=False)
    incident_type = db.Column(db.String(100), nullable=False)  # phone_use, sleeping, disruptive, etc.
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high
    description = db.Column(db.Text)
    action_taken = db.Column(db.Text)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'date': self.date.isoformat() if self.date else None,
            'incident_type': self.incident_type,
            'severity': self.severity,
            'description': self.description,
            'action_taken': self.action_taken,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Contact(db.Model):
    """Contact information model (parents, counselors, etc.)"""
    __tablename__ = 'contacts'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    name = db.Column(db.String(200), nullable=False)
    relationship = db.Column(db.String(50), nullable=False)  # parent, guardian, counselor, assistant_principal, special_ed
    email = db.Column(db.String(200))
    phone = db.Column(db.String(20))
    is_primary = db.Column(db.Boolean, default=False)
    receive_alerts = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'name': self.name,
            'relationship': self.relationship,
            'email': self.email,
            'phone': self.phone,
            'is_primary': self.is_primary,
            'receive_alerts': self.receive_alerts,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


class Alert(db.Model):
    """Alert log model"""
    __tablename__ = 'alerts'
    
    id = db.Column(db.Integer, primary_key=True)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    alert_type = db.Column(db.String(50), nullable=False)  # attendance, grade, behavior, assignment
    severity = db.Column(db.String(20), nullable=False)  # low, medium, high, critical
    message = db.Column(db.Text, nullable=False)
    sent_to = db.Column(db.Text)  # JSON list of email addresses
    sent_at = db.Column(db.DateTime, default=datetime.utcnow)
    
    student = db.relationship('Student', backref='alerts')
    
    def to_dict(self):
        return {
            'id': self.id,
            'student_id': self.student_id,
            'alert_type': self.alert_type,
            'severity': self.severity,
            'message': self.message,
            'sent_to': self.sent_to,
            'sent_at': self.sent_at.isoformat() if self.sent_at else None
        }
