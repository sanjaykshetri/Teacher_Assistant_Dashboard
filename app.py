"""
Teacher Assistant Dashboard - Main Flask Application
"""
import os
from datetime import datetime
from flask import Flask, jsonify, request, send_from_directory
from flask_cors import CORS
from dotenv import load_dotenv
from models import db, Student, Attendance, Grade, Assignment, Behavior, Contact, Alert
from alert_system import AlertSystem

# Load environment variables
load_dotenv()

app = Flask(__name__, static_folder='static', static_url_path='')
CORS(app)

# Configuration
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'dev-secret-key')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///teacher_dashboard.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
alert_system = AlertSystem(app)


@app.route('/')
def index():
    """Serve the main dashboard page"""
    return send_from_directory('static', 'index.html')


# Student endpoints
@app.route('/api/students', methods=['GET', 'POST'])
def students():
    """Get all students or create a new student"""
    if request.method == 'GET':
        students = Student.query.all()
        return jsonify([s.to_dict() for s in students])
    
    elif request.method == 'POST':
        data = request.json
        student = Student(
            first_name=data['first_name'],
            last_name=data['last_name'],
            student_id=data['student_id'],
            grade_level=data.get('grade_level'),
            special_ed=data.get('special_ed', False),
            accommodations=data.get('accommodations')
        )
        db.session.add(student)
        db.session.commit()
        return jsonify(student.to_dict()), 201


@app.route('/api/students/<int:student_id>', methods=['GET', 'PUT', 'DELETE'])
def student_detail(student_id):
    """Get, update, or delete a specific student"""
    student = Student.query.get_or_404(student_id)
    
    if request.method == 'GET':
        return jsonify(student.to_dict())
    
    elif request.method == 'PUT':
        data = request.json
        student.first_name = data.get('first_name', student.first_name)
        student.last_name = data.get('last_name', student.last_name)
        student.student_id = data.get('student_id', student.student_id)
        student.grade_level = data.get('grade_level', student.grade_level)
        student.special_ed = data.get('special_ed', student.special_ed)
        student.accommodations = data.get('accommodations', student.accommodations)
        db.session.commit()
        return jsonify(student.to_dict())
    
    elif request.method == 'DELETE':
        db.session.delete(student)
        db.session.commit()
        return '', 204


@app.route('/api/students/<int:student_id>/dashboard', methods=['GET'])
def student_dashboard(student_id):
    """Get comprehensive dashboard data for a student"""
    student = Student.query.get_or_404(student_id)
    
    # Get recent data
    recent_attendance = Attendance.query.filter_by(student_id=student_id).order_by(Attendance.date.desc()).limit(10).all()
    recent_grades = Grade.query.filter_by(student_id=student_id).order_by(Grade.date.desc()).limit(10).all()
    recent_assignments = Assignment.query.filter_by(student_id=student_id).order_by(Assignment.due_date.desc()).limit(10).all()
    recent_behaviors = Behavior.query.filter_by(student_id=student_id).order_by(Behavior.date.desc()).limit(10).all()
    contacts = Contact.query.filter_by(student_id=student_id).all()
    recent_alerts = Alert.query.filter_by(student_id=student_id).order_by(Alert.sent_at.desc()).limit(10).all()
    
    return jsonify({
        'student': student.to_dict(),
        'attendance': [a.to_dict() for a in recent_attendance],
        'grades': [g.to_dict() for g in recent_grades],
        'assignments': [a.to_dict() for a in recent_assignments],
        'behaviors': [b.to_dict() for b in recent_behaviors],
        'contacts': [c.to_dict() for c in contacts],
        'alerts': [a.to_dict() for a in recent_alerts]
    })


# Attendance endpoints
@app.route('/api/attendance', methods=['GET', 'POST'])
def attendance():
    """Get all attendance records or create a new record"""
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        query = Attendance.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        records = query.order_by(Attendance.date.desc()).all()
        return jsonify([r.to_dict() for r in records])
    
    elif request.method == 'POST':
        data = request.json
        record = Attendance(
            student_id=data['student_id'],
            date=datetime.fromisoformat(data['date']).date(),
            status=data['status'],
            notes=data.get('notes')
        )
        db.session.add(record)
        db.session.commit()
        return jsonify(record.to_dict()), 201


# Grade endpoints
@app.route('/api/grades', methods=['GET', 'POST'])
def grades():
    """Get all grades or create a new grade"""
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        query = Grade.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        records = query.order_by(Grade.date.desc()).all()
        return jsonify([r.to_dict() for r in records])
    
    elif request.method == 'POST':
        data = request.json
        grade = Grade(
            student_id=data['student_id'],
            subject=data['subject'],
            assignment_name=data['assignment_name'],
            score=data['score'],
            max_score=data['max_score'],
            date=datetime.fromisoformat(data['date']).date(),
            notes=data.get('notes')
        )
        db.session.add(grade)
        db.session.commit()
        return jsonify(grade.to_dict()), 201


# Assignment endpoints
@app.route('/api/assignments', methods=['GET', 'POST'])
def assignments():
    """Get all assignments or create a new assignment"""
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        query = Assignment.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        records = query.order_by(Assignment.due_date.desc()).all()
        return jsonify([r.to_dict() for r in records])
    
    elif request.method == 'POST':
        data = request.json
        assignment = Assignment(
            student_id=data['student_id'],
            title=data['title'],
            description=data.get('description'),
            due_date=datetime.fromisoformat(data['due_date']).date(),
            submitted=data.get('submitted', False),
            submission_date=datetime.fromisoformat(data['submission_date']).date() if data.get('submission_date') else None,
            status=data['status']
        )
        db.session.add(assignment)
        db.session.commit()
        return jsonify(assignment.to_dict()), 201


# Behavior endpoints
@app.route('/api/behaviors', methods=['GET', 'POST'])
def behaviors():
    """Get all behavior records or create a new record"""
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        query = Behavior.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        records = query.order_by(Behavior.date.desc()).all()
        return jsonify([r.to_dict() for r in records])
    
    elif request.method == 'POST':
        data = request.json
        behavior = Behavior(
            student_id=data['student_id'],
            date=datetime.fromisoformat(data['date']).date(),
            incident_type=data['incident_type'],
            severity=data['severity'],
            description=data.get('description'),
            action_taken=data.get('action_taken')
        )
        db.session.add(behavior)
        db.session.commit()
        return jsonify(behavior.to_dict()), 201


# Contact endpoints
@app.route('/api/contacts', methods=['GET', 'POST'])
def contacts():
    """Get all contacts or create a new contact"""
    if request.method == 'GET':
        student_id = request.args.get('student_id')
        query = Contact.query
        if student_id:
            query = query.filter_by(student_id=student_id)
        records = query.all()
        return jsonify([r.to_dict() for r in records])
    
    elif request.method == 'POST':
        data = request.json
        contact = Contact(
            student_id=data['student_id'],
            name=data['name'],
            relationship=data['relationship'],
            email=data.get('email'),
            phone=data.get('phone'),
            is_primary=data.get('is_primary', False),
            receive_alerts=data.get('receive_alerts', True)
        )
        db.session.add(contact)
        db.session.commit()
        return jsonify(contact.to_dict()), 201


# Alert endpoints
@app.route('/api/alerts', methods=['GET'])
def alerts():
    """Get all alerts"""
    student_id = request.args.get('student_id')
    query = Alert.query
    if student_id:
        query = query.filter_by(student_id=student_id)
    records = query.order_by(Alert.sent_at.desc()).all()
    return jsonify([r.to_dict() for r in records])


@app.route('/api/alerts/check', methods=['POST'])
def check_alerts():
    """Manually trigger alert checks"""
    alerts = alert_system.run_all_checks()
    return jsonify({
        'message': f'Checked all students. Generated {len(alerts)} alerts.',
        'alerts': [a.to_dict() for a in alerts]
    })


# Dashboard summary endpoint
@app.route('/api/dashboard/summary', methods=['GET'])
def dashboard_summary():
    """Get overall dashboard summary statistics"""
    total_students = Student.query.count()
    total_alerts = Alert.query.count()
    
    # Recent alerts by severity
    recent_alerts = Alert.query.order_by(Alert.sent_at.desc()).limit(20).all()
    alerts_by_severity = {
        'critical': sum(1 for a in recent_alerts if a.severity == 'critical'),
        'high': sum(1 for a in recent_alerts if a.severity == 'high'),
        'medium': sum(1 for a in recent_alerts if a.severity == 'medium'),
        'low': sum(1 for a in recent_alerts if a.severity == 'low')
    }
    
    # Students with issues
    students_with_alerts = db.session.query(Alert.student_id).distinct().count()
    
    return jsonify({
        'total_students': total_students,
        'total_alerts': total_alerts,
        'alerts_by_severity': alerts_by_severity,
        'students_with_alerts': students_with_alerts,
        'recent_alerts': [a.to_dict() for a in recent_alerts]
    })


def init_db():
    """Initialize the database"""
    with app.app_context():
        db.create_all()
        print("Database initialized!")


if __name__ == '__main__':
    init_db()
    # Debug mode should only be enabled in development
    # Set FLASK_ENV=development in .env for debug mode
    debug_mode = os.getenv('FLASK_ENV') == 'development'
    app.run(debug=debug_mode, host='0.0.0.0', port=5000)
