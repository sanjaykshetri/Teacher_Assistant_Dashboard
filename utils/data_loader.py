"""
Data loader utilities for student records.
"""
import pandas as pd
import os
from typing import Dict, Tuple


def get_data_path(filename: str) -> str:
    """Get the full path to a data file."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)
    return os.path.join(project_root, "data", filename)


def load_student_data() -> pd.DataFrame:
    """Load student information."""
    return pd.read_csv(get_data_path("students.csv"))


def load_grades_data() -> pd.DataFrame:
    """Load grades data."""
    df = pd.read_csv(get_data_path("grades.csv"))
    df['date'] = pd.to_datetime(df['date'])
    return df


def load_attendance_data() -> pd.DataFrame:
    """Load attendance data."""
    df = pd.read_csv(get_data_path("attendance.csv"))
    df['date'] = pd.to_datetime(df['date'])
    return df


def load_behavior_data() -> pd.DataFrame:
    """Load behavior data."""
    df = pd.read_csv(get_data_path("behavior.csv"))
    df['date'] = pd.to_datetime(df['date'])
    return df


def load_all_data() -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all data at once."""
    return (
        load_student_data(),
        load_grades_data(),
        load_attendance_data(),
        load_behavior_data()
    )


def calculate_student_average(grades_df: pd.DataFrame, student_id: int) -> float:
    """Calculate average grade for a student."""
    student_grades = grades_df[grades_df['student_id'] == student_id]
    if len(student_grades) == 0:
        return 0.0
    
    # Calculate percentage for each assignment
    student_grades = student_grades.copy()
    student_grades['percentage'] = (student_grades['score'] / student_grades['max_score']) * 100
    return student_grades['percentage'].mean()


def calculate_attendance_rate(attendance_df: pd.DataFrame, student_id: int) -> float:
    """Calculate attendance rate for a student."""
    student_attendance = attendance_df[attendance_df['student_id'] == student_id]
    if len(student_attendance) == 0:
        return 100.0
    
    present_count = len(student_attendance[student_attendance['status'] == 'present'])
    total_count = len(student_attendance)
    return (present_count / total_count) * 100


def count_behavior_incidents(behavior_df: pd.DataFrame, student_id: int, incident_type: str = None) -> int:
    """Count behavior incidents for a student."""
    student_behavior = behavior_df[behavior_df['student_id'] == student_id]
    if incident_type:
        student_behavior = student_behavior[student_behavior['incident_type'] == incident_type]
    return len(student_behavior)


def get_student_summary(student_id: int) -> Dict:
    """Get a comprehensive summary for a student."""
    students_df, grades_df, attendance_df, behavior_df = load_all_data()
    
    student = students_df[students_df['student_id'] == student_id].iloc[0]
    
    return {
        'student_id': student_id,
        'name': student['name'],
        'email': student['email'],
        'parent_name': student['parent_name'],
        'parent_email': student['parent_email'],
        'grade_level': student['grade_level'],
        'average_grade': calculate_student_average(grades_df, student_id),
        'attendance_rate': calculate_attendance_rate(attendance_df, student_id),
        'positive_incidents': count_behavior_incidents(behavior_df, student_id, 'positive'),
        'negative_incidents': count_behavior_incidents(behavior_df, student_id, 'disruption'),
    }
