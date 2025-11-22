"""
Email generation utilities for student communications.
"""
from typing import Dict, List
import pandas as pd
from datetime import datetime


class EmailGenerator:
    """Generate emails based on student performance."""
    
    # Thresholds for triggering emails
    LOW_GRADE_THRESHOLD = 70.0
    CRITICAL_GRADE_THRESHOLD = 60.0
    LOW_ATTENDANCE_THRESHOLD = 80.0
    CRITICAL_ATTENDANCE_THRESHOLD = 70.0
    MULTIPLE_INCIDENTS_THRESHOLD = 2
    
    def __init__(self, teacher_name: str = "Mr./Ms. Teacher", teacher_email: str = "teacher@school.edu"):
        self.teacher_name = teacher_name
        self.teacher_email = teacher_email
        self.assistant_principal_email = "assistant.principal@school.edu"
    
    def should_send_email(self, student_summary: Dict) -> Dict[str, bool]:
        """Determine which emails should be sent based on student performance."""
        grade = student_summary['average_grade']
        attendance = student_summary['attendance_rate']
        negative_incidents = student_summary['negative_incidents']
        
        return {
            'to_parent': (
                grade < self.LOW_GRADE_THRESHOLD or 
                attendance < self.LOW_ATTENDANCE_THRESHOLD or 
                negative_incidents >= self.MULTIPLE_INCIDENTS_THRESHOLD
            ),
            'to_student': (
                grade < self.LOW_GRADE_THRESHOLD or 
                attendance < self.LOW_ATTENDANCE_THRESHOLD
            ),
            'to_admin': (
                grade < self.CRITICAL_GRADE_THRESHOLD or 
                attendance < self.CRITICAL_ATTENDANCE_THRESHOLD or 
                negative_incidents >= 3
            )
        }
    
    def generate_parent_email(self, student_summary: Dict) -> Dict[str, str]:
        """Generate email to parent."""
        name = student_summary['name']
        parent_name = student_summary['parent_name']
        grade = student_summary['average_grade']
        attendance = student_summary['attendance_rate']
        negative_incidents = student_summary['negative_incidents']
        positive_incidents = student_summary['positive_incidents']
        
        # Determine concerns
        concerns = []
        if grade < self.CRITICAL_GRADE_THRESHOLD:
            concerns.append(f"academic performance (current average: {grade:.1f}%)")
        elif grade < self.LOW_GRADE_THRESHOLD:
            concerns.append(f"academic performance (current average: {grade:.1f}%)")
        
        if attendance < self.CRITICAL_ATTENDANCE_THRESHOLD:
            concerns.append(f"attendance (current rate: {attendance:.1f}%)")
        elif attendance < self.LOW_ATTENDANCE_THRESHOLD:
            concerns.append(f"attendance (current rate: {attendance:.1f}%)")
        
        if negative_incidents >= self.MULTIPLE_INCIDENTS_THRESHOLD:
            concerns.append(f"classroom behavior ({negative_incidents} incident(s) recorded)")
        
        # Build subject
        if len(concerns) > 0:
            subject = f"Concerns Regarding {name}'s Performance"
            tone = "concerned"
        else:
            subject = f"Update on {name}'s Progress"
            tone = "positive"
        
        # Build body
        body = f"Dear {parent_name},\n\n"
        
        if tone == "concerned":
            body += f"I hope this email finds you well. I am writing to discuss some concerns regarding {name}'s performance in my class.\n\n"
            body += "Areas of concern:\n"
            for concern in concerns:
                body += f"• {concern.capitalize()}\n"
            body += f"\n"
            
            if positive_incidents > 0:
                body += f"I want to acknowledge that {name} has also shown positive behavior with {positive_incidents} positive incident(s) recorded.\n\n"
            
            body += f"I believe that with some additional support and attention, {name} can improve in these areas. "
            body += f"I would appreciate the opportunity to discuss strategies we can implement together to help {name} succeed.\n\n"
            body += f"Please feel free to contact me to schedule a meeting or phone call at your earliest convenience.\n\n"
        else:
            body += f"I wanted to take a moment to provide you with a positive update on {name}'s progress.\n\n"
            body += f"Current performance:\n"
            body += f"• Academic average: {grade:.1f}%\n"
            body += f"• Attendance rate: {attendance:.1f}%\n"
            if positive_incidents > 0:
                body += f"• Positive behavior incidents: {positive_incidents}\n"
            body += f"\n{name} is doing well and I'm pleased with their progress. Keep up the great work!\n\n"
        
        body += f"Best regards,\n{self.teacher_name}\n{self.teacher_email}"
        
        return {
            'subject': subject,
            'body': body,
            'to': student_summary['parent_email'],
            'recipient_name': parent_name
        }
    
    def generate_student_email(self, student_summary: Dict) -> Dict[str, str]:
        """Generate email to student."""
        name = student_summary['name']
        grade = student_summary['average_grade']
        attendance = student_summary['attendance_rate']
        
        # Build subject
        if grade < self.LOW_GRADE_THRESHOLD or attendance < self.LOW_ATTENDANCE_THRESHOLD:
            subject = f"Let's Talk About Your Progress"
        else:
            subject = f"Great Work on Your Progress!"
        
        # Build body
        body = f"Dear {name},\n\n"
        
        if grade < self.CRITICAL_GRADE_THRESHOLD:
            body += f"I wanted to reach out regarding your current academic standing. Your current average is {grade:.1f}%, "
            body += f"and I'm concerned about your progress.\n\n"
            body += f"I'm here to help you succeed! Let's work together to identify areas where you're struggling and develop "
            body += f"a plan to improve your grades. Please come see me during office hours or after class.\n\n"
        elif grade < self.LOW_GRADE_THRESHOLD:
            body += f"I noticed your current average is {grade:.1f}%. While you're passing, I believe you have the potential "
            body += f"to do better!\n\n"
            body += f"Let's meet to discuss strategies for improving your performance. Small changes can make a big difference.\n\n"
        else:
            body += f"I wanted to commend you on your excellent work! Your current average of {grade:.1f}% demonstrates your "
            body += f"dedication and hard work.\n\n"
        
        if attendance < self.LOW_ATTENDANCE_THRESHOLD:
            body += f"I've also noticed your attendance has been a concern at {attendance:.1f}%. Regular attendance is crucial "
            body += f"for your success. Please let me know if there's anything I can do to support you.\n\n"
        
        body += f"Remember, I'm here to help you succeed. Don't hesitate to reach out if you need assistance.\n\n"
        body += f"Best regards,\n{self.teacher_name}\n{self.teacher_email}"
        
        return {
            'subject': subject,
            'body': body,
            'to': student_summary['email'],
            'recipient_name': name
        }
    
    def generate_admin_email(self, student_summary: Dict) -> Dict[str, str]:
        """Generate email to assistant principal."""
        name = student_summary['name']
        grade = student_summary['average_grade']
        attendance = student_summary['attendance_rate']
        negative_incidents = student_summary['negative_incidents']
        
        subject = f"Student Concern: {name} - Requires Attention"
        
        body = f"Dear Assistant Principal,\n\n"
        body += f"I am writing to bring to your attention concerns regarding {name} (Student ID: {student_summary['student_id']}, "
        body += f"Grade {student_summary['grade_level']}).\n\n"
        body += f"Current Status:\n"
        body += f"• Academic Average: {grade:.1f}%\n"
        body += f"• Attendance Rate: {attendance:.1f}%\n"
        body += f"• Behavioral Incidents: {negative_incidents}\n\n"
        
        body += f"Areas of concern:\n"
        if grade < self.CRITICAL_GRADE_THRESHOLD:
            body += f"• Academic performance is critically low and may result in course failure\n"
        if attendance < self.CRITICAL_ATTENDANCE_THRESHOLD:
            body += f"• Attendance is critically low and impacting learning\n"
        if negative_incidents >= 3:
            body += f"• Multiple behavioral incidents requiring administrative intervention\n"
        
        body += f"\nI have contacted the parents and student regarding these concerns. However, I believe administrative "
        body += f"support and intervention may be necessary to ensure this student's success.\n\n"
        body += f"Please let me know if you would like to schedule a meeting to discuss next steps.\n\n"
        body += f"Best regards,\n{self.teacher_name}\n{self.teacher_email}"
        
        return {
            'subject': subject,
            'body': body,
            'to': self.assistant_principal_email,
            'recipient_name': 'Assistant Principal'
        }
    
    def generate_all_emails(self, student_summary: Dict) -> Dict[str, Dict]:
        """Generate all applicable emails for a student."""
        should_send = self.should_send_email(student_summary)
        emails = {}
        
        if should_send['to_parent']:
            emails['parent'] = self.generate_parent_email(student_summary)
        
        if should_send['to_student']:
            emails['student'] = self.generate_student_email(student_summary)
        
        if should_send['to_admin']:
            emails['admin'] = self.generate_admin_email(student_summary)
        
        return emails
