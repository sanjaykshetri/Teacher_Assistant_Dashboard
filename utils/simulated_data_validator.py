"""
Validation utilities for the simulated multi-table dataset.
"""

from __future__ import annotations

import os
from typing import Dict, Iterable, Optional, Set

import pandas as pd


class SimulatedDataValidator:
    """Validate the normalized simulated dataset under data/sim_data/csv_unpacked."""

    def __init__(self, data_dir: str = "data") -> None:
        self.data_dir = data_dir
        self.sim_data_dir = os.path.join(data_dir, "sim_data", "csv_unpacked")
        self.errors = []
        self.warnings = []

        self.required_files = [
            "students.csv",
            "courses.csv",
            "enrollments.csv",
            "assignments.csv",
            "assignment_scores.csv",
            "assessments.csv",
            "assessment_scores.csv",
            "attendance.csv",
            "behavior_incidents.csv",
            "interventions.csv",
            "grade_snapshots.csv",
            "data_dictionary.csv",
        ]

        self.required_columns = {
            "students": [
                "student_id", "first_name", "last_name", "preferred_name", "grade_level",
                "student_email", "guardian_name", "guardian_email", "ell_status",
                "iep_504_status", "baseline_math_level",
            ],
            "courses": ["course_id", "course_name", "school_year", "term", "period", "room", "teacher_name"],
            "enrollments": ["enrollment_id", "student_id", "course_id", "enrollment_start", "enrollment_end"],
            "assignments": [
                "assignment_id", "course_id", "assignment_title", "assignment_type", "unit",
                "date_assigned", "date_due", "points_possible",
            ],
            "assignment_scores": [
                "score_id", "student_id", "course_id", "assignment_id", "date_submitted",
                "submission_status", "points_possible", "points_earned", "missing_flag", "late_flag",
            ],
            "assessments": [
                "assessment_id", "course_id", "assessment_title", "assessment_type", "unit",
                "assessment_date", "points_possible",
            ],
            "assessment_scores": [
                "assessment_score_id", "student_id", "course_id", "assessment_id",
                "points_possible", "points_earned", "retake_flag",
            ],
            "attendance": ["attendance_id", "student_id", "course_id", "date", "status", "minutes_late", "excused_flag"],
            "behavior_incidents": [
                "incident_id", "student_id", "course_id", "date", "incident_type", "severity",
                "action_taken", "notes",
            ],
            "interventions": [
                "intervention_id", "student_id", "course_id", "date", "intervention_type",
                "assigned_by", "follow_up_date", "outcome",
            ],
            "grade_snapshots": [
                "snapshot_id", "student_id", "course_id", "week_number", "current_grade_pct",
                "assignment_avg_pct", "assessment_avg_pct", "missing_assignments", "late_assignments",
                "absences", "tardies", "behavior_incidents", "risk_band", "recommended_next_step",
            ],
            "data_dictionary": ["table", "primary_key", "grain", "notes"],
        }

    def _file_path(self, filename: str) -> str:
        return os.path.join(self.sim_data_dir, filename)

    def _validate_file_presence(self) -> bool:
        ok = True
        for filename in self.required_files:
            path = self._file_path(filename)
            if not os.path.exists(path):
                self.errors.append(f"Missing required file: {path}")
                ok = False
        return ok

    def _load_csv(self, filename: str) -> Optional[pd.DataFrame]:
        path = self._file_path(filename)
        if not os.path.exists(path):
            return None
        return pd.read_csv(path)

    def _require_columns(self, df: pd.DataFrame, table: str) -> bool:
        required = self.required_columns[table]
        missing = [col for col in required if col not in df.columns]
        if missing:
            self.errors.append(f"{table}.csv missing columns: {missing}")
            return False
        return True

    def _check_unique(self, df: pd.DataFrame, table: str, key_col: str) -> None:
        dupes = df[df.duplicated(key_col, keep=False)]
        if not dupes.empty:
            values = dupes[key_col].astype(str).unique().tolist()
            self.errors.append(f"{table}.csv has duplicate {key_col} values: {values[:10]}")

    def _check_fk(self, df: pd.DataFrame, table: str, col: str, valid_values: Set[str], target: str) -> None:
        unknown = df[~df[col].astype(str).isin(valid_values)]
        if not unknown.empty:
            vals = unknown[col].astype(str).unique().tolist()
            self.errors.append(f"{table}.csv has unknown {col} values not in {target}: {vals[:10]}")

    def _check_allowed(self, df: pd.DataFrame, table: str, col: str, allowed: Iterable[str], allow_blank: bool = False) -> None:
        allowed_set = {v.lower() for v in allowed}
        series = df[col].fillna("").astype(str).str.strip().str.lower()
        if allow_blank:
            bad = series[(series != "") & (~series.isin(allowed_set))]
        else:
            bad = series[~series.isin(allowed_set)]
        if not bad.empty:
            values = sorted(bad.unique().tolist())
            self.errors.append(f"{table}.csv has invalid values in {col}: {values}")

    def _check_date_column(self, df: pd.DataFrame, table: str, col: str, allow_blank: bool = False) -> None:
        raw = df[col].fillna("").astype(str).str.strip()
        parsed = pd.to_datetime(raw, format="%Y-%m-%d", errors="coerce")
        if allow_blank:
            invalid_mask = (raw != "") & parsed.isna()
        else:
            invalid_mask = parsed.isna()
        if invalid_mask.any():
            self.warnings.append(f"{table}.csv has invalid date values in {col}: {int(invalid_mask.sum())} row(s)")

    def _check_non_negative(self, df: pd.DataFrame, table: str, col: str) -> None:
        values = pd.to_numeric(df[col], errors="coerce")
        if values.isna().any():
            self.errors.append(f"{table}.csv has non-numeric values in {col}")
            return
        if (values < 0).any():
            self.errors.append(f"{table}.csv has negative values in {col}")

    def _check_points_consistency(self, df: pd.DataFrame, table: str, earned_col: str, possible_col: str) -> None:
        earned = pd.to_numeric(df[earned_col], errors="coerce")
        possible = pd.to_numeric(df[possible_col], errors="coerce")
        if earned.isna().any() or possible.isna().any():
            self.errors.append(f"{table}.csv has non-numeric score columns")
            return
        if (possible <= 0).any():
            self.errors.append(f"{table}.csv has non-positive {possible_col} values")
        if (earned < 0).any():
            self.errors.append(f"{table}.csv has negative {earned_col} values")
        if (earned > possible).any():
            self.errors.append(f"{table}.csv has {earned_col} > {possible_col} values")

    def run_all_validations(self) -> bool:
        print("=" * 60)
        print("SIMULATED DATA VALIDATION REPORT")
        print("=" * 60)

        if not self._validate_file_presence():
            self._print_summary()
            return False

        tables: Dict[str, pd.DataFrame] = {}
        for table in [f.replace(".csv", "") for f in self.required_files]:
            df = self._load_csv(f"{table}.csv")
            if df is None:
                continue
            tables[table] = df
            if not self._require_columns(df, table):
                self._print_summary()
                return False
            if len(df) == 0:
                self.warnings.append(f"{table}.csv is empty")

        students = tables["students"]
        courses = tables["courses"]
        enrollments = tables["enrollments"]
        assignments = tables["assignments"]
        assignment_scores = tables["assignment_scores"]
        assessments = tables["assessments"]
        assessment_scores = tables["assessment_scores"]
        attendance = tables["attendance"]
        behavior = tables["behavior_incidents"]
        interventions = tables["interventions"]
        snapshots = tables["grade_snapshots"]
        dictionary = tables["data_dictionary"]

        print(f"Loaded simulated rows: students={len(students)}, courses={len(courses)}, enrollments={len(enrollments)}")

        self._check_unique(students, "students", "student_id")
        self._check_unique(courses, "courses", "course_id")
        self._check_unique(enrollments, "enrollments", "enrollment_id")
        self._check_unique(assignments, "assignments", "assignment_id")
        self._check_unique(assignment_scores, "assignment_scores", "score_id")
        self._check_unique(assessments, "assessments", "assessment_id")
        self._check_unique(assessment_scores, "assessment_scores", "assessment_score_id")
        self._check_unique(attendance, "attendance", "attendance_id")
        self._check_unique(behavior, "behavior_incidents", "incident_id")
        self._check_unique(interventions, "interventions", "intervention_id")
        self._check_unique(snapshots, "grade_snapshots", "snapshot_id")

        student_ids = set(students["student_id"].astype(str))
        course_ids = set(courses["course_id"].astype(str))
        assignment_ids = set(assignments["assignment_id"].astype(str))
        assessment_ids = set(assessments["assessment_id"].astype(str))

        self._check_fk(enrollments, "enrollments", "student_id", student_ids, "students.student_id")
        self._check_fk(enrollments, "enrollments", "course_id", course_ids, "courses.course_id")
        shared_course_ids = set(course_ids)
        shared_course_ids.add("ALL")
        self._check_fk(assignments, "assignments", "course_id", shared_course_ids, "courses.course_id or ALL")
        self._check_fk(assessments, "assessments", "course_id", shared_course_ids, "courses.course_id or ALL")
        self._check_fk(assignment_scores, "assignment_scores", "student_id", student_ids, "students.student_id")
        self._check_fk(assignment_scores, "assignment_scores", "course_id", course_ids, "courses.course_id")
        self._check_fk(assignment_scores, "assignment_scores", "assignment_id", assignment_ids, "assignments.assignment_id")
        self._check_fk(assessment_scores, "assessment_scores", "student_id", student_ids, "students.student_id")
        self._check_fk(assessment_scores, "assessment_scores", "course_id", course_ids, "courses.course_id")
        self._check_fk(assessment_scores, "assessment_scores", "assessment_id", assessment_ids, "assessments.assessment_id")
        self._check_fk(attendance, "attendance", "student_id", student_ids, "students.student_id")
        self._check_fk(attendance, "attendance", "course_id", course_ids, "courses.course_id")
        self._check_fk(behavior, "behavior_incidents", "student_id", student_ids, "students.student_id")
        self._check_fk(behavior, "behavior_incidents", "course_id", course_ids, "courses.course_id")
        self._check_fk(interventions, "interventions", "student_id", student_ids, "students.student_id")
        self._check_fk(interventions, "interventions", "course_id", course_ids, "courses.course_id")
        self._check_fk(snapshots, "grade_snapshots", "student_id", student_ids, "students.student_id")
        self._check_fk(snapshots, "grade_snapshots", "course_id", course_ids, "courses.course_id")

        self._check_allowed(attendance, "attendance", "status", ["Present", "Absent", "Tardy"])
        self._check_allowed(attendance, "attendance", "excused_flag", ["Yes", "No"], allow_blank=True)
        self._check_allowed(assignment_scores, "assignment_scores", "submission_status", ["Submitted", "Late", "Missing"])
        self._check_allowed(assignment_scores, "assignment_scores", "missing_flag", ["Yes", "No"])
        self._check_allowed(assignment_scores, "assignment_scores", "late_flag", ["Yes", "No"])
        self._check_allowed(assessment_scores, "assessment_scores", "retake_flag", ["Yes", "No"])
        self._check_allowed(behavior, "behavior_incidents", "severity", ["Low", "Medium", "High"])
        self._check_allowed(snapshots, "grade_snapshots", "risk_band", ["Low", "Medium", "High"])

        for table, col, allow_blank in [
            ("enrollments", "enrollment_start", False),
            ("enrollments", "enrollment_end", True),
            ("assignments", "date_assigned", False),
            ("assignments", "date_due", False),
            ("assessments", "assessment_date", False),
            ("assignment_scores", "date_submitted", True),
            ("attendance", "date", False),
            ("behavior_incidents", "date", False),
            ("interventions", "date", False),
            ("interventions", "follow_up_date", True),
        ]:
            self._check_date_column(tables[table], table, col, allow_blank=allow_blank)

        self._check_non_negative(attendance, "attendance", "minutes_late")
        self._check_non_negative(snapshots, "grade_snapshots", "week_number")
        self._check_non_negative(snapshots, "grade_snapshots", "missing_assignments")
        self._check_non_negative(snapshots, "grade_snapshots", "late_assignments")
        self._check_non_negative(snapshots, "grade_snapshots", "absences")
        self._check_non_negative(snapshots, "grade_snapshots", "tardies")
        self._check_non_negative(snapshots, "grade_snapshots", "behavior_incidents")

        self._check_points_consistency(assignments, "assignments", "points_possible", "points_possible")
        self._check_points_consistency(assessments, "assessments", "points_possible", "points_possible")
        self._check_points_consistency(assignment_scores, "assignment_scores", "points_earned", "points_possible")
        self._check_points_consistency(assessment_scores, "assessment_scores", "points_earned", "points_possible")

        expected_tables = {
            "students", "courses", "enrollments", "assignments", "assignment_scores", "assessments",
            "assessment_scores", "attendance", "behavior_incidents", "interventions", "grade_snapshots",
        }
        declared_tables = set(dictionary["table"].dropna().astype(str).str.strip())
        missing_decl = sorted(expected_tables - declared_tables)
        if missing_decl:
            self.warnings.append(f"data_dictionary.csv missing table entries: {missing_decl}")

        self._print_summary()
        return len(self.errors) == 0

    def _print_summary(self) -> None:
        print("\n" + "=" * 60)
        print("SUMMARY")
        print("=" * 60)

        if self.errors:
            print(f"\nERRORS ({len(self.errors)}):")
            for err in self.errors:
                print(f"  - {err}")

        if self.warnings:
            print(f"\nWARNINGS ({len(self.warnings)}):")
            for warn in self.warnings:
                print(f"  - {warn}")

        if not self.errors and not self.warnings:
            print("\nAll simulated data files validated successfully.")
        elif not self.errors:
            print("\nNo critical errors found for simulated data. Review warnings.")
        else:
            print("\nSimulated data has critical validation errors.")

        print("=" * 60)
