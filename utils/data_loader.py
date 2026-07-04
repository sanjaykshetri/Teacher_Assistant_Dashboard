"""
Data loader utilities for student records.
"""
import pandas as pd
import os
from typing import Dict, Tuple, Optional


DATA_SOURCE_LEGACY = "legacy"
DATA_SOURCE_SIMULATED = "simulated"


def get_data_path(filename: str, data_source: str = DATA_SOURCE_LEGACY) -> str:
    """Get the full path to a data file for the requested source."""
    current_dir = os.path.dirname(os.path.abspath(__file__))
    project_root = os.path.dirname(current_dir)

    if data_source == DATA_SOURCE_SIMULATED:
        return os.path.join(project_root, "data", "sim_data", "csv_unpacked", filename)

    return os.path.join(project_root, "data", filename)


def _load_legacy_student_data() -> pd.DataFrame:
    """Load legacy student information."""
    return pd.read_csv(get_data_path("students.csv", DATA_SOURCE_LEGACY))


def _load_simulated_student_data() -> pd.DataFrame:
    """Load simulated student information and normalize to legacy schema."""
    df = pd.read_csv(get_data_path("students.csv", DATA_SOURCE_SIMULATED))

    # Build a display name that prefers preferred_name when available.
    preferred = df["preferred_name"].fillna("").astype(str).str.strip()
    full_name = (
        df["first_name"].fillna("").astype(str).str.strip() +
        " " +
        df["last_name"].fillna("").astype(str).str.strip()
    ).str.strip()

    normalized = pd.DataFrame({
        "student_id": df["student_id"],
        "name": preferred.where(preferred != "", full_name),
        "email": df["student_email"],
        "parent_name": df["guardian_name"],
        "parent_email": df["guardian_email"],
        "grade_level": df["grade_level"],
    })
    return normalized


def load_student_data(data_source: str = DATA_SOURCE_LEGACY) -> pd.DataFrame:
    """Load student information from the selected source."""
    if data_source == DATA_SOURCE_SIMULATED:
        return _load_simulated_student_data()
    return _load_legacy_student_data()


def _load_legacy_grades_data() -> pd.DataFrame:
    """Load legacy grades data."""
    df = pd.read_csv(get_data_path("grades.csv", DATA_SOURCE_LEGACY))
    df['date'] = pd.to_datetime(df['date'])
    return df


def _load_simulated_grades_data() -> pd.DataFrame:
    """Load simulated assignment and assessment scores as a single grades table."""
    assignments = pd.read_csv(get_data_path("assignments.csv", DATA_SOURCE_SIMULATED))
    assignment_scores = pd.read_csv(get_data_path("assignment_scores.csv", DATA_SOURCE_SIMULATED))
    assessments = pd.read_csv(get_data_path("assessments.csv", DATA_SOURCE_SIMULATED))
    assessment_scores = pd.read_csv(get_data_path("assessment_scores.csv", DATA_SOURCE_SIMULATED))

    assignment_joined = assignment_scores.merge(
        assignments[["assignment_id", "assignment_title", "assignment_type", "date_due"]],
        on="assignment_id",
        how="left"
    )
    assignment_dates = pd.to_datetime(
        assignment_joined["date_submitted"].where(
            assignment_joined["date_submitted"].notna() & (assignment_joined["date_submitted"] != ""),
            assignment_joined["date_due"]
        )
    )

    assignment_grades = pd.DataFrame({
        "student_id": assignment_joined["student_id"],
        "assignment_name": assignment_joined["assignment_title"],
        "assignment_type": assignment_joined["assignment_type"],
        "score": assignment_joined["points_earned"].fillna(0),
        "max_score": assignment_joined["points_possible"].fillna(0),
        "date": assignment_dates,
    })

    assessment_joined = assessment_scores.merge(
        assessments[["assessment_id", "assessment_title", "assessment_type", "assessment_date"]],
        on="assessment_id",
        how="left"
    )

    assessment_grades = pd.DataFrame({
        "student_id": assessment_joined["student_id"],
        "assignment_name": assessment_joined["assessment_title"],
        "assignment_type": assessment_joined["assessment_type"],
        "score": assessment_joined["points_earned"].fillna(0),
        "max_score": assessment_joined["points_possible"].fillna(0),
        "date": pd.to_datetime(assessment_joined["assessment_date"]),
    })

    combined = pd.concat([assignment_grades, assessment_grades], ignore_index=True)
    combined["assignment_type"] = combined["assignment_type"].fillna("other").astype(str).str.lower()
    return combined


def load_grades_data(data_source: str = DATA_SOURCE_LEGACY) -> pd.DataFrame:
    """Load grades data from the selected source."""
    if data_source == DATA_SOURCE_SIMULATED:
        return _load_simulated_grades_data()
    return _load_legacy_grades_data()


def _load_legacy_attendance_data() -> pd.DataFrame:
    """Load legacy attendance data."""
    df = pd.read_csv(get_data_path("attendance.csv", DATA_SOURCE_LEGACY))
    df['date'] = pd.to_datetime(df['date'])
    return df


def _load_simulated_attendance_data() -> pd.DataFrame:
    """Load simulated attendance data and normalize to legacy schema."""
    df = pd.read_csv(get_data_path("attendance.csv", DATA_SOURCE_SIMULATED))
    normalized = pd.DataFrame({
        "student_id": df["student_id"],
        "date": pd.to_datetime(df["date"]),
        "status": df["status"].fillna("present").astype(str).str.lower(),
        "notes": df.apply(
            lambda row: f"Late by {int(row['minutes_late'])} minute(s)" if str(row.get("status", "")).lower() == "tardy" else (
                "Excused absence" if str(row.get("excused_flag", "")).lower() == "yes" else ""
            ),
            axis=1
        )
    })
    return normalized


def load_attendance_data(data_source: str = DATA_SOURCE_LEGACY) -> pd.DataFrame:
    """Load attendance data from the selected source."""
    if data_source == DATA_SOURCE_SIMULATED:
        return _load_simulated_attendance_data()
    return _load_legacy_attendance_data()


def _load_legacy_behavior_data() -> pd.DataFrame:
    """Load legacy behavior data."""
    df = pd.read_csv(get_data_path("behavior.csv", DATA_SOURCE_LEGACY))
    df['date'] = pd.to_datetime(df['date'])
    return df


def _load_simulated_behavior_data() -> pd.DataFrame:
    """Load simulated behavior incidents and normalize to legacy schema."""
    df = pd.read_csv(get_data_path("behavior_incidents.csv", DATA_SOURCE_SIMULATED))
    normalized = pd.DataFrame({
        "student_id": df["student_id"],
        "date": pd.to_datetime(df["date"]),
        "incident_type": df["incident_type"].fillna("other").astype(str).str.lower(),
        "severity": df["severity"].fillna("low").astype(str).str.lower(),
        "description": (
            "Action: " + df["action_taken"].fillna("").astype(str) +
            "; Notes: " + df["notes"].fillna("").astype(str)
        ).str.strip("; "),
    })
    return normalized


def load_behavior_data(data_source: str = DATA_SOURCE_LEGACY) -> pd.DataFrame:
    """Load behavior data from the selected source."""
    if data_source == DATA_SOURCE_SIMULATED:
        return _load_simulated_behavior_data()
    return _load_legacy_behavior_data()


def load_all_data(data_source: str = DATA_SOURCE_LEGACY) -> Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """Load all data at once from the selected source."""
    return (
        load_student_data(data_source),
        load_grades_data(data_source),
        load_attendance_data(data_source),
        load_behavior_data(data_source)
    )


def calculate_student_average(grades_df: pd.DataFrame, student_id) -> float:
    """Calculate average grade for a student."""
    student_grades = grades_df[grades_df['student_id'] == student_id]
    if len(student_grades) == 0:
        return 0.0
    
    # Calculate percentage for each assignment
    student_grades = student_grades.copy()
    student_grades['percentage'] = (student_grades['score'] / student_grades['max_score']) * 100
    return student_grades['percentage'].mean()


def calculate_attendance_rate(attendance_df: pd.DataFrame, student_id) -> float:
    """Calculate attendance rate for a student."""
    student_attendance = attendance_df[attendance_df['student_id'] == student_id]
    if len(student_attendance) == 0:
        return 100.0
    
    present_count = len(student_attendance[student_attendance['status'] == 'present'])
    total_count = len(student_attendance)
    return (present_count / total_count) * 100


def count_behavior_incidents(behavior_df: pd.DataFrame, student_id, incident_type: Optional[str] = None) -> int:
    """Count behavior incidents for a student."""
    student_behavior = behavior_df[behavior_df['student_id'] == student_id]
    if incident_type:
        student_behavior = student_behavior[student_behavior['incident_type'] == incident_type]
    return len(student_behavior)


def get_student_summary(
    student_id,
    data_source: str = DATA_SOURCE_LEGACY,
    preloaded_data: Optional[Tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, pd.DataFrame]] = None
) -> Dict:
    """Get a comprehensive summary for a student."""
    if preloaded_data is None:
        students_df, grades_df, attendance_df, behavior_df = load_all_data(data_source)
    else:
        students_df, grades_df, attendance_df, behavior_df = preloaded_data
    
    student_rows = students_df[students_df['student_id'] == student_id]
    if len(student_rows) == 0:
        raise ValueError(f"Student ID {student_id} not found")
    student = student_rows.iloc[0]
    
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
        # Treat all non-positive incidents as negative so both legacy and simulated data are supported.
        'negative_incidents': count_behavior_incidents(behavior_df, student_id) - count_behavior_incidents(behavior_df, student_id, 'positive'),
    }
