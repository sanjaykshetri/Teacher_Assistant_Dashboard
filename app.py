"""
Teacher Assistant Dashboard - Main Application
A Streamlit dashboard for managing student records and generating automated emails.
"""
import streamlit as st
import pandas as pd
from utils.data_loader import (
    load_all_data,
    get_student_summary,
    calculate_student_average,
    calculate_attendance_rate,
    count_behavior_incidents
)
from utils.email_generator import EmailGenerator

# Page configuration
st.set_page_config(
    page_title="Teacher Assistant Dashboard",
    page_icon="📚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Initialize email generator
if 'email_generator' not in st.session_state:
    st.session_state.email_generator = EmailGenerator(
        teacher_name="Mr./Ms. Teacher",
        teacher_email="teacher@school.edu"
    )

# Load data
@st.cache_data
def get_data():
    """Load and cache all data."""
    return load_all_data()

students_df, grades_df, attendance_df, behavior_df = get_data()

# Sidebar navigation
st.sidebar.title("📚 Teacher Assistant")
st.sidebar.markdown("---")

page = st.sidebar.radio(
    "Navigation",
    ["Dashboard", "Student Records", "Email Generator", "Batch Email Generation"]
)

st.sidebar.markdown("---")
st.sidebar.markdown("### Settings")
teacher_name = st.sidebar.text_input("Teacher Name", value="Mr./Ms. Teacher")
teacher_email = st.sidebar.text_input("Teacher Email", value="teacher@school.edu")

if teacher_name != st.session_state.email_generator.teacher_name or \
   teacher_email != st.session_state.email_generator.teacher_email:
    st.session_state.email_generator = EmailGenerator(teacher_name, teacher_email)

# Main content
if page == "Dashboard":
    st.title("📊 Teacher Assistant Dashboard")
    st.markdown("### Student Performance Overview")
    
    # Calculate summary statistics for all students
    summary_data = []
    for _, student in students_df.iterrows():
        student_id = student['student_id']
        summary = get_student_summary(student_id)
        summary_data.append(summary)
    
    summary_df = pd.DataFrame(summary_data)
    
    # Display key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total Students", len(students_df))
    
    with col2:
        avg_grade = summary_df['average_grade'].mean()
        st.metric("Class Average", f"{avg_grade:.1f}%")
    
    with col3:
        avg_attendance = summary_df['attendance_rate'].mean()
        st.metric("Average Attendance", f"{avg_attendance:.1f}%")
    
    with col4:
        students_at_risk = len(summary_df[
            (summary_df['average_grade'] < 70) | 
            (summary_df['attendance_rate'] < 80)
        ])
        st.metric("Students At Risk", students_at_risk)
    
    st.markdown("---")
    
    # Student summary table
    st.markdown("### Student Summary")
    
    # Format the display dataframe
    display_df = summary_df[['name', 'grade_level', 'average_grade', 'attendance_rate', 
                             'positive_incidents', 'negative_incidents']].copy()
    display_df.columns = ['Name', 'Grade Level', 'Avg Grade (%)', 'Attendance (%)', 
                          'Positive', 'Negative']
    display_df['Avg Grade (%)'] = display_df['Avg Grade (%)'].round(1)
    display_df['Attendance (%)'] = display_df['Attendance (%)'].round(1)
    
    # Color code based on performance
    def highlight_performance(row):
        colors = [''] * len(row)
        if row['Avg Grade (%)'] < 60:
            colors[2] = 'background-color: #ffcccc'
        elif row['Avg Grade (%)'] < 70:
            colors[2] = 'background-color: #ffffcc'
        
        if row['Attendance (%)'] < 70:
            colors[3] = 'background-color: #ffcccc'
        elif row['Attendance (%)'] < 80:
            colors[3] = 'background-color: #ffffcc'
        
        if row['Negative'] >= 3:
            colors[5] = 'background-color: #ffcccc'
        elif row['Negative'] >= 2:
            colors[5] = 'background-color: #ffffcc'
        
        return colors
    
    styled_df = display_df.style.apply(highlight_performance, axis=1)
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    st.markdown("""
    **Color Legend:**
    - 🟥 Red: Critical (Grade < 60%, Attendance < 70%, or 3+ negative incidents)
    - 🟨 Yellow: Warning (Grade < 70%, Attendance < 80%, or 2+ negative incidents)
    """)

elif page == "Student Records":
    st.title("📋 Student Records")
    
    # Student selector
    student_names = students_df['name'].tolist()
    selected_student_name = st.selectbox("Select a student", student_names)
    
    # Get student details
    student = students_df[students_df['name'] == selected_student_name].iloc[0]
    student_id = student['student_id']
    
    # Display student information
    st.markdown(f"## {student['name']}")
    
    col1, col2 = st.columns(2)
    with col1:
        st.markdown("**Student Information**")
        st.write(f"**Student ID:** {student_id}")
        st.write(f"**Email:** {student['email']}")
        st.write(f"**Grade Level:** {student['grade_level']}")
    
    with col2:
        st.markdown("**Parent Information**")
        st.write(f"**Parent Name:** {student['parent_name']}")
        st.write(f"**Parent Email:** {student['parent_email']}")
    
    st.markdown("---")
    
    # Performance summary
    summary = get_student_summary(student_id)
    
    col1, col2, col3 = st.columns(3)
    with col1:
        grade_color = "🟢" if summary['average_grade'] >= 70 else ("🟡" if summary['average_grade'] >= 60 else "🔴")
        st.metric("Average Grade", f"{summary['average_grade']:.1f}%", delta=None)
        st.markdown(grade_color)
    
    with col2:
        attendance_color = "🟢" if summary['attendance_rate'] >= 80 else ("🟡" if summary['attendance_rate'] >= 70 else "🔴")
        st.metric("Attendance Rate", f"{summary['attendance_rate']:.1f}%", delta=None)
        st.markdown(attendance_color)
    
    with col3:
        st.metric("Behavior", f"+{summary['positive_incidents']} / -{summary['negative_incidents']}")
    
    st.markdown("---")
    
    # Detailed records tabs
    tab1, tab2, tab3 = st.tabs(["📝 Grades", "📅 Attendance", "⚠️ Behavior"])
    
    with tab1:
        student_grades = grades_df[grades_df['student_id'] == student_id].copy()
        if not student_grades.empty:
            student_grades['percentage'] = (student_grades['score'] / student_grades['max_score'] * 100).round(1)
            student_grades['date'] = student_grades['date'].dt.strftime('%Y-%m-%d')
            display_grades = student_grades[['date', 'assignment_name', 'assignment_type', 'score', 'max_score', 'percentage']]
            display_grades.columns = ['Date', 'Assignment', 'Type', 'Score', 'Max Score', 'Percentage']
            st.dataframe(display_grades, use_container_width=True, hide_index=True)
        else:
            st.info("No grade records found.")
    
    with tab2:
        student_attendance = attendance_df[attendance_df['student_id'] == student_id].copy()
        if not student_attendance.empty:
            student_attendance['date'] = student_attendance['date'].dt.strftime('%Y-%m-%d')
            display_attendance = student_attendance[['date', 'status', 'notes']]
            display_attendance.columns = ['Date', 'Status', 'Notes']
            st.dataframe(display_attendance, use_container_width=True, hide_index=True)
            
            # Attendance summary
            status_counts = student_attendance['status'].value_counts()
            st.markdown("**Attendance Summary:**")
            for status, count in status_counts.items():
                st.write(f"- {status.capitalize()}: {count}")
        else:
            st.info("No attendance records found.")
    
    with tab3:
        student_behavior = behavior_df[behavior_df['student_id'] == student_id].copy()
        if not student_behavior.empty:
            student_behavior['date'] = student_behavior['date'].dt.strftime('%Y-%m-%d')
            display_behavior = student_behavior[['date', 'incident_type', 'severity', 'description']]
            display_behavior.columns = ['Date', 'Type', 'Severity', 'Description']
            st.dataframe(display_behavior, use_container_width=True, hide_index=True)
        else:
            st.info("No behavior records found.")

elif page == "Email Generator":
    st.title("✉️ Email Generator")
    st.markdown("Generate personalized emails for students, parents, and administrators.")
    
    # Student selector
    student_names = students_df['name'].tolist()
    selected_student_name = st.selectbox("Select a student", student_names)
    
    # Get student details
    student = students_df[students_df['name'] == selected_student_name].iloc[0]
    student_id = student['student_id']
    summary = get_student_summary(student_id)
    
    st.markdown("---")
    st.markdown(f"### Student Performance Summary: {summary['name']}")
    
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Average Grade", f"{summary['average_grade']:.1f}%")
    with col2:
        st.metric("Attendance Rate", f"{summary['attendance_rate']:.1f}%")
    with col3:
        st.metric("Behavior Incidents", f"+{summary['positive_incidents']} / -{summary['negative_incidents']}")
    
    st.markdown("---")
    
    # Check which emails should be sent
    email_gen = st.session_state.email_generator
    should_send = email_gen.should_send_email(summary)
    
    st.markdown("### Recommended Communications")
    col1, col2, col3 = st.columns(3)
    with col1:
        st.write("**To Parent:**", "✅ Yes" if should_send['to_parent'] else "❌ No")
    with col2:
        st.write("**To Student:**", "✅ Yes" if should_send['to_student'] else "❌ No")
    with col3:
        st.write("**To Admin:**", "✅ Yes" if should_send['to_admin'] else "❌ No")
    
    st.markdown("---")
    
    # Generate and display emails
    emails = email_gen.generate_all_emails(summary)
    
    if emails:
        st.markdown("### Generated Emails")
        
        for recipient_type, email_data in emails.items():
            with st.expander(f"📧 Email to {recipient_type.capitalize()}", expanded=True):
                st.markdown(f"**To:** {email_data['to']}")
                st.markdown(f"**Subject:** {email_data['subject']}")
                st.markdown("**Body:**")
                st.text_area(
                    f"email_body_{recipient_type}",
                    value=email_data['body'],
                    height=300,
                    label_visibility="collapsed"
                )
                
                if st.button(f"Copy {recipient_type.capitalize()} Email", key=f"copy_{recipient_type}"):
                    st.info(f"Email content ready to copy! (In a production environment, this would copy to clipboard)")
    else:
        st.success("✅ No immediate concerns detected. This student is performing well!")
        st.info("You can still generate positive feedback emails by adjusting the thresholds or manually creating communications.")

elif page == "Batch Email Generation":
    st.title("📬 Batch Email Generation")
    st.markdown("Generate emails for all students who need attention.")
    
    # Calculate which students need emails
    students_needing_attention = []
    email_gen = st.session_state.email_generator
    
    for _, student in students_df.iterrows():
        student_id = student['student_id']
        summary = get_student_summary(student_id)
        should_send = email_gen.should_send_email(summary)
        
        if should_send['to_parent'] or should_send['to_student'] or should_send['to_admin']:
            students_needing_attention.append({
                'student_id': student_id,
                'name': summary['name'],
                'average_grade': summary['average_grade'],
                'attendance_rate': summary['attendance_rate'],
                'negative_incidents': summary['negative_incidents'],
                'to_parent': should_send['to_parent'],
                'to_student': should_send['to_student'],
                'to_admin': should_send['to_admin']
            })
    
    if students_needing_attention:
        st.markdown(f"### Students Requiring Communication: {len(students_needing_attention)}")
        
        # Display summary table
        summary_table = pd.DataFrame(students_needing_attention)
        display_cols = ['name', 'average_grade', 'attendance_rate', 'negative_incidents', 'to_parent', 'to_student', 'to_admin']
        display_table = summary_table[display_cols].copy()
        display_table.columns = ['Name', 'Avg Grade', 'Attendance', 'Incidents', 'Parent Email', 'Student Email', 'Admin Email']
        display_table['Avg Grade'] = display_table['Avg Grade'].round(1)
        display_table['Attendance'] = display_table['Attendance'].round(1)
        
        st.dataframe(display_table, use_container_width=True, hide_index=True)
        
        st.markdown("---")
        
        # Generate all emails button
        if st.button("Generate All Emails", type="primary"):
            st.markdown("### All Generated Emails")
            
            for student_info in students_needing_attention:
                student_id = student_info['student_id']
                summary = get_student_summary(student_id)
                emails = email_gen.generate_all_emails(summary)
                
                st.markdown(f"## {summary['name']}")
                
                for recipient_type, email_data in emails.items():
                    with st.expander(f"📧 {recipient_type.capitalize()} Email"):
                        st.markdown(f"**To:** {email_data['to']}")
                        st.markdown(f"**Subject:** {email_data['subject']}")
                        st.markdown("**Body:**")
                        st.text_area(
                            f"batch_email_{student_id}_{recipient_type}",
                            value=email_data['body'],
                            height=250,
                            label_visibility="collapsed"
                        )
                
                st.markdown("---")
            
            st.success(f"✅ Generated emails for {len(students_needing_attention)} students!")
    else:
        st.success("🎉 Great news! No students currently require attention emails.")
        st.info("All students are performing within acceptable parameters.")

# Footer
st.sidebar.markdown("---")
st.sidebar.markdown("### About")
st.sidebar.info(
    "Teacher Assistant Dashboard v1.0\n\n"
    "This dashboard helps teachers manage student records and generate "
    "automated emails based on performance, attendance, and behavior data."
)
