"""
Data Validation Script for Teacher Assistant Dashboard
Checks CSV files for common errors and data integrity issues
"""

import argparse
import pandas as pd
import os
from datetime import datetime
import re

try:
    from utils.simulated_data_validator import SimulatedDataValidator
except ImportError:
    from simulated_data_validator import SimulatedDataValidator

class DataValidator:
    def __init__(self, data_dir='data'):
        self.data_dir = data_dir
        self.errors = []
        self.warnings = []
        
    def validate_email(self, email):
        """Validate email format"""
        if pd.isna(email):
            return False
        pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(pattern, str(email)) is not None
    
    def validate_date(self, date_str):
        """Validate date format (YYYY-MM-DD)"""
        if pd.isna(date_str):
            return False
        try:
            datetime.strptime(str(date_str), '%Y-%m-%d')
            return True
        except ValueError:
            return False
    
    def validate_students(self):
        """Validate students.csv"""
        print("\n📋 Validating students.csv...")
        filepath = os.path.join(self.data_dir, 'students.csv')
        
        if not os.path.exists(filepath):
            self.errors.append("❌ students.csv not found")
            return
        
        df = pd.read_csv(filepath)
        
        # Check required columns
        required_cols = ['student_id', 'name', 'email', 'parent_name', 'parent_email', 'grade_level']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"❌ Missing columns in students.csv: {missing_cols}")
            return
        
        # Check for duplicate student IDs
        duplicates = df[df.duplicated('student_id', keep=False)]
        if not duplicates.empty:
            self.errors.append(f"❌ Duplicate student IDs found: {duplicates['student_id'].tolist()}")
        
        # Validate emails
        for idx, row in df.iterrows():
            if not self.validate_email(row['email']):
                self.warnings.append(f"⚠️  Invalid student email at row {idx+2}: {row['email']}")
            if not self.validate_email(row['parent_email']):
                self.warnings.append(f"⚠️  Invalid parent email at row {idx+2}: {row['parent_email']}")
        
        # Check grade levels
        invalid_grades = df[~df['grade_level'].isin([9, 10, 11, 12])]
        if not invalid_grades.empty:
            self.warnings.append(f"⚠️  Invalid grade levels found: {invalid_grades['grade_level'].tolist()}")
        
        # Check for missing data
        for col in required_cols:
            missing = df[df[col].isna()]
            if not missing.empty:
                self.errors.append(f"❌ Missing {col} for {len(missing)} student(s)")
        
        print(f"✓ Found {len(df)} students")
    
    def validate_grades(self):
        """Validate grades.csv"""
        print("\n📊 Validating grades.csv...")
        filepath = os.path.join(self.data_dir, 'grades.csv')
        
        if not os.path.exists(filepath):
            self.errors.append("❌ grades.csv not found")
            return
        
        df = pd.read_csv(filepath)
        students_df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
        valid_student_ids = students_df['student_id'].tolist()
        
        # Check required columns
        required_cols = ['student_id', 'assignment_name', 'assignment_type', 'score', 'max_score', 'date']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"❌ Missing columns in grades.csv: {missing_cols}")
            return
        
        # Validate student IDs exist
        invalid_ids = df[~df['student_id'].isin(valid_student_ids)]
        if not invalid_ids.empty:
            self.errors.append(f"❌ Unknown student IDs in grades: {invalid_ids['student_id'].unique().tolist()}")
        
        # Validate assignment types
        valid_types = ['quiz', 'assignment', 'exam', 'project', 'homework']
        invalid_types = df[~df['assignment_type'].isin(valid_types)]
        if not invalid_types.empty:
            self.warnings.append(f"⚠️  Non-standard assignment types: {invalid_types['assignment_type'].unique().tolist()}")
        
        # Validate scores
        invalid_scores = df[df['score'] > df['max_score']]
        if not invalid_scores.empty:
            self.errors.append(f"❌ {len(invalid_scores)} grade(s) have score > max_score")
        
        negative_scores = df[(df['score'] < 0) | (df['max_score'] <= 0)]
        if not negative_scores.empty:
            self.errors.append(f"❌ {len(negative_scores)} grade(s) have negative or zero values")
        
        # Validate dates
        for idx, row in df.iterrows():
            if not self.validate_date(row['date']):
                self.warnings.append(f"⚠️  Invalid date format at row {idx+2}: {row['date']}")
        
        print(f"✓ Found {len(df)} grade entries")
    
    def validate_attendance(self):
        """Validate attendance.csv"""
        print("\n📅 Validating attendance.csv...")
        filepath = os.path.join(self.data_dir, 'attendance.csv')
        
        if not os.path.exists(filepath):
            self.errors.append("❌ attendance.csv not found")
            return
        
        df = pd.read_csv(filepath)
        students_df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
        valid_student_ids = students_df['student_id'].tolist()
        
        # Check required columns
        required_cols = ['student_id', 'date', 'status']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"❌ Missing columns in attendance.csv: {missing_cols}")
            return
        
        # Validate student IDs
        invalid_ids = df[~df['student_id'].isin(valid_student_ids)]
        if not invalid_ids.empty:
            self.errors.append(f"❌ Unknown student IDs in attendance: {invalid_ids['student_id'].unique().tolist()}")
        
        # Validate status values
        valid_statuses = ['present', 'absent', 'tardy', 'excused']
        invalid_statuses = df[~df['status'].isin(valid_statuses)]
        if not invalid_statuses.empty:
            self.errors.append(f"❌ Invalid status values: {invalid_statuses['status'].unique().tolist()}")
        
        # Validate dates
        for idx, row in df.iterrows():
            if not self.validate_date(row['date']):
                self.warnings.append(f"⚠️  Invalid date format at row {idx+2}: {row['date']}")
        
        # Check for duplicate entries (same student, same date)
        duplicates = df[df.duplicated(['student_id', 'date'], keep=False)]
        if not duplicates.empty:
            self.warnings.append(f"⚠️  {len(duplicates)} duplicate attendance entries found")
        
        print(f"✓ Found {len(df)} attendance records")
    
    def validate_behavior(self):
        """Validate behavior.csv"""
        print("\n📝 Validating behavior.csv...")
        filepath = os.path.join(self.data_dir, 'behavior.csv')
        
        if not os.path.exists(filepath):
            self.errors.append("❌ behavior.csv not found")
            return
        
        df = pd.read_csv(filepath)
        students_df = pd.read_csv(os.path.join(self.data_dir, 'students.csv'))
        valid_student_ids = students_df['student_id'].tolist()
        
        # Check required columns
        required_cols = ['student_id', 'date', 'incident_type', 'severity', 'description']
        missing_cols = [col for col in required_cols if col not in df.columns]
        if missing_cols:
            self.errors.append(f"❌ Missing columns in behavior.csv: {missing_cols}")
            return
        
        # Validate student IDs
        invalid_ids = df[~df['student_id'].isin(valid_student_ids)]
        if not invalid_ids.empty:
            self.errors.append(f"❌ Unknown student IDs in behavior: {invalid_ids['student_id'].unique().tolist()}")
        
        # Validate incident types
        valid_types = ['positive', 'disruption', 'tardy', 'unprepared', 'other']
        invalid_types = df[~df['incident_type'].isin(valid_types)]
        if not invalid_types.empty:
            self.warnings.append(f"⚠️  Non-standard incident types: {invalid_types['incident_type'].unique().tolist()}")
        
        # Validate severity
        valid_severities = ['low', 'medium', 'high']
        invalid_severities = df[~df['severity'].isin(valid_severities)]
        if not invalid_severities.empty:
            self.errors.append(f"❌ Invalid severity values: {invalid_severities['severity'].unique().tolist()}")
        
        # Validate dates
        for idx, row in df.iterrows():
            if not self.validate_date(row['date']):
                self.warnings.append(f"⚠️  Invalid date format at row {idx+2}: {row['date']}")
        
        # Check for missing descriptions
        missing_desc = df[df['description'].isna()]
        if not missing_desc.empty:
            self.warnings.append(f"⚠️  {len(missing_desc)} behavior entries missing description")
        
        print(f"✓ Found {len(df)} behavior records")
    
    def run_all_validations(self):
        """Run all validation checks"""
        print("="*60)
        print("🔍 DATA VALIDATION REPORT")
        print("="*60)
        
        self.validate_students()
        self.validate_grades()
        self.validate_attendance()
        self.validate_behavior()
        
        print("\n" + "="*60)
        print("📊 SUMMARY")
        print("="*60)
        
        if self.errors:
            print(f"\n❌ ERRORS ({len(self.errors)}):")
            for error in self.errors:
                print(f"  {error}")
        
        if self.warnings:
            print(f"\n⚠️  WARNINGS ({len(self.warnings)}):")
            for warning in self.warnings:
                print(f"  {warning}")
        
        if not self.errors and not self.warnings:
            print("\n✅ All data files validated successfully! No errors or warnings.")
        elif not self.errors:
            print("\n✅ No critical errors found. Please review warnings.")
        else:
            print("\n❌ Please fix the errors above before using the dashboard.")
        
        print("="*60)
        
        return len(self.errors) == 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Validate legacy CSV data, simulated normalized data, or both datasets."
    )
    parser.add_argument(
        "--data-source",
        choices=["legacy", "simulated", "both"],
        default="legacy",
        help="Select which dataset to validate (default: legacy)."
    )
    parser.add_argument(
        "--data-dir",
        default="data",
        help="Base data directory (default: data)."
    )
    args = parser.parse_args()

    if args.data_source == "legacy":
        success = DataValidator(data_dir=args.data_dir).run_all_validations()
    elif args.data_source == "simulated":
        success = SimulatedDataValidator(data_dir=args.data_dir).run_all_validations()
    else:
        print("Running legacy validation...\n")
        legacy_ok = DataValidator(data_dir=args.data_dir).run_all_validations()
        print("\nRunning simulated validation...\n")
        simulated_ok = SimulatedDataValidator(data_dir=args.data_dir).run_all_validations()

        success = legacy_ok and simulated_ok
        print("\n" + "=" * 60)
        print("OVERALL RESULT")
        print("=" * 60)
        if success:
            print("All selected validations passed.")
        else:
            print("One or more selected validations failed.")
        print("=" * 60)

    exit(0 if success else 1)
