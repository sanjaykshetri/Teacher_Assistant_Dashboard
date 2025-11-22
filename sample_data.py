"""
Script to populate the database with sample data for demonstration
"""
from datetime import datetime, timedelta
import random
from app import app, db
from models import Student, Attendance, Grade, Assignment, Behavior, Contact

def create_sample_data():
    """Create sample data for the dashboard"""
    
    with app.app_context():
        # Clear existing data
        print("Clearing existing data...")
        db.drop_all()
        db.create_all()
        
        # Create sample students
        print("Creating sample students...")
        students = [
            Student(
                first_name='John',
                last_name='Smith',
                student_id='STU001',
                grade_level=10,
                special_ed=False,
                accommodations=None
            ),
            Student(
                first_name='Emma',
                last_name='Johnson',
                student_id='STU002',
                grade_level=11,
                special_ed=True,
                accommodations='Extended time on tests, preferential seating'
            ),
            Student(
                first_name='Michael',
                last_name='Williams',
                student_id='STU003',
                grade_level=9,
                special_ed=False,
                accommodations=None
            ),
            Student(
                first_name='Sophia',
                last_name='Brown',
                student_id='STU004',
                grade_level=10,
                special_ed=False,
                accommodations=None
            ),
            Student(
                first_name='James',
                last_name='Davis',
                student_id='STU005',
                grade_level=12,
                special_ed=True,
                accommodations='Note-taking assistance, oral testing option'
            )
        ]
        
        for student in students:
            db.session.add(student)
        db.session.commit()
        
        # Create sample contacts
        print("Creating sample contacts...")
        contacts_data = [
            # John Smith contacts
            {'student_id': 1, 'name': 'Robert Smith', 'relationship': 'parent', 'email': 'robert.smith@email.com', 'phone': '555-0101', 'is_primary': True},
            {'student_id': 1, 'name': 'Sarah Smith', 'relationship': 'parent', 'email': 'sarah.smith@email.com', 'phone': '555-0102'},
            {'student_id': 1, 'name': 'Ms. Anderson', 'relationship': 'counselor', 'email': 'anderson@school.edu', 'phone': '555-0201'},
            
            # Emma Johnson contacts
            {'student_id': 2, 'name': 'Linda Johnson', 'relationship': 'parent', 'email': 'linda.johnson@email.com', 'phone': '555-0103', 'is_primary': True},
            {'student_id': 2, 'name': 'Mr. Martinez', 'relationship': 'special_ed', 'email': 'martinez@school.edu', 'phone': '555-0202'},
            {'student_id': 2, 'name': 'Dr. Thompson', 'relationship': 'counselor', 'email': 'thompson@school.edu', 'phone': '555-0203'},
            
            # Michael Williams contacts
            {'student_id': 3, 'name': 'David Williams', 'relationship': 'parent', 'email': 'david.williams@email.com', 'phone': '555-0104', 'is_primary': True},
            {'student_id': 3, 'name': 'Mr. Garcia', 'relationship': 'assistant_principal', 'email': 'garcia@school.edu', 'phone': '555-0204'},
            
            # Sophia Brown contacts
            {'student_id': 4, 'name': 'Jennifer Brown', 'relationship': 'parent', 'email': 'jennifer.brown@email.com', 'phone': '555-0105', 'is_primary': True},
            {'student_id': 4, 'name': 'Ms. Lee', 'relationship': 'counselor', 'email': 'lee@school.edu', 'phone': '555-0205'},
            
            # James Davis contacts
            {'student_id': 5, 'name': 'Patricia Davis', 'relationship': 'guardian', 'email': 'patricia.davis@email.com', 'phone': '555-0106', 'is_primary': True},
            {'student_id': 5, 'name': 'Mr. Martinez', 'relationship': 'special_ed', 'email': 'martinez@school.edu', 'phone': '555-0202'},
        ]
        
        for contact_data in contacts_data:
            contact = Contact(**contact_data)
            db.session.add(contact)
        db.session.commit()
        
        # Create sample attendance records (past 30 days)
        print("Creating sample attendance records...")
        attendance_statuses = ['present', 'absent', 'tardy', 'present', 'present', 'present', 'present']
        
        for i in range(30):
            date = datetime.now().date() - timedelta(days=i)
            for student in students:
                # Student 2 (Emma) has more absences
                if student.id == 2:
                    status = random.choice(['present', 'absent', 'tardy', 'present', 'absent'])
                # Student 3 (Michael) has some tardies
                elif student.id == 3:
                    status = random.choice(['present', 'tardy', 'present', 'present', 'tardy'])
                else:
                    status = random.choice(attendance_statuses)
                
                attendance = Attendance(
                    student_id=student.id,
                    date=date,
                    status=status,
                    notes='Excused' if status == 'absent' and random.random() > 0.7 else None
                )
                db.session.add(attendance)
        db.session.commit()
        
        # Create sample grades
        print("Creating sample grades...")
        subjects = ['Mathematics', 'English', 'Science', 'History', 'Physical Education']
        assignment_types = ['Quiz', 'Test', 'Homework', 'Project', 'Essay']
        
        for i in range(60):
            date = datetime.now().date() - timedelta(days=random.randint(0, 60))
            for student in students:
                subject = random.choice(subjects)
                assignment_type = random.choice(assignment_types)
                
                # Student 2 and 5 have some lower grades
                if student.id in [2, 5]:
                    score = random.randint(50, 100)
                else:
                    score = random.randint(70, 100)
                
                max_score = 100
                
                grade = Grade(
                    student_id=student.id,
                    subject=subject,
                    assignment_name=f'{subject} {assignment_type} {i}',
                    score=score,
                    max_score=max_score,
                    date=date
                )
                db.session.add(grade)
        db.session.commit()
        
        # Create sample assignments
        print("Creating sample assignments...")
        assignment_titles = [
            'Chapter 5 Reading',
            'Math Problem Set',
            'Science Lab Report',
            'History Essay',
            'Book Report',
            'Research Project'
        ]
        
        for i in range(20):
            due_date = datetime.now().date() + timedelta(days=random.randint(-10, 30))
            for student in students:
                # Some students have missing assignments
                if student.id in [3, 5] and random.random() > 0.7:
                    status = 'missing'
                    submitted = False
                elif due_date < datetime.now().date():
                    status = random.choice(['submitted', 'late', 'missing'])
                    submitted = status in ['submitted', 'late']
                else:
                    status = 'pending'
                    submitted = False
                
                assignment = Assignment(
                    student_id=student.id,
                    title=random.choice(assignment_titles),
                    description=f'Assignment for student {student.first_name}',
                    due_date=due_date,
                    submitted=submitted,
                    submission_date=due_date if submitted else None,
                    status=status
                )
                db.session.add(assignment)
        db.session.commit()
        
        # Create sample behavior incidents
        print("Creating sample behavior incidents...")
        incident_types = ['phone_use', 'sleeping', 'disruptive', 'tardiness', 'talking_out']
        severities = ['low', 'medium', 'high']
        
        # Student 3 (Michael) has multiple behavior issues
        for i in range(5):
            date = datetime.now().date() - timedelta(days=random.randint(0, 14))
            behavior = Behavior(
                student_id=3,
                date=date,
                incident_type=random.choice(incident_types),
                severity=random.choice(['medium', 'high']),
                description='Repeated violation of classroom rules',
                action_taken='Parent contact, detention assigned'
            )
            db.session.add(behavior)
        
        # Student 2 (Emma) has a few incidents
        for i in range(2):
            date = datetime.now().date() - timedelta(days=random.randint(0, 14))
            behavior = Behavior(
                student_id=2,
                date=date,
                incident_type='phone_use',
                severity='low',
                description='Phone out during class',
                action_taken='Verbal warning'
            )
            db.session.add(behavior)
        
        # Random incidents for other students
        for student in [1, 4, 5]:
            if random.random() > 0.5:
                date = datetime.now().date() - timedelta(days=random.randint(0, 30))
                behavior = Behavior(
                    student_id=student,
                    date=date,
                    incident_type=random.choice(incident_types),
                    severity=random.choice(severities),
                    description='Minor classroom incident',
                    action_taken='Discussion with student'
                )
                db.session.add(behavior)
        
        db.session.commit()
        
        print("Sample data created successfully!")
        print("\nSummary:")
        print(f"Students: {Student.query.count()}")
        print(f"Contacts: {Contact.query.count()}")
        print(f"Attendance Records: {Attendance.query.count()}")
        print(f"Grades: {Grade.query.count()}")
        print(f"Assignments: {Assignment.query.count()}")
        print(f"Behavior Incidents: {Behavior.query.count()}")

if __name__ == '__main__':
    create_sample_data()
