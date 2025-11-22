// API Base URL
const API_BASE = '/api';

// Global state
let studentsMap = {};

// Load dashboard on page load
document.addEventListener('DOMContentLoaded', () => {
    loadDashboard();
});

// Load all dashboard data
async function loadDashboard() {
    try {
        await Promise.all([
            loadSummary(),
            loadStudents(),
            loadAlerts(),
            loadAttendance(),
            loadGrades(),
            loadBehaviors()
        ]);
        showMessage('Dashboard loaded successfully', 'success');
    } catch (error) {
        console.error('Error loading dashboard:', error);
        showMessage('Error loading dashboard data', 'error');
    }
}

// Load summary statistics
async function loadSummary() {
    try {
        const response = await fetch(`${API_BASE}/dashboard/summary`);
        const data = await response.json();
        
        document.getElementById('totalStudents').textContent = data.total_students;
        document.getElementById('totalAlerts').textContent = data.total_alerts;
        document.getElementById('highAlerts').textContent = data.alerts_by_severity.high;
        document.getElementById('mediumAlerts').textContent = data.alerts_by_severity.medium;
    } catch (error) {
        console.error('Error loading summary:', error);
    }
}

// Load students
async function loadStudents() {
    try {
        const response = await fetch(`${API_BASE}/students`);
        const students = await response.json();
        
        // Build students map for easy lookup
        studentsMap = {};
        students.forEach(student => {
            studentsMap[student.id] = student;
        });
        
        const tbody = document.getElementById('studentsTableBody');
        tbody.innerHTML = '';
        
        students.forEach(student => {
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${student.student_id}</td>
                <td>${student.first_name} ${student.last_name}</td>
                <td>${student.grade_level || 'N/A'}</td>
                <td>${student.special_ed ? '✓' : ''}</td>
                <td>
                    <button onclick="viewStudent(${student.id})" class="btn btn-primary" style="padding: 5px 15px;">View</button>
                </td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading students:', error);
    }
}

// Load alerts
async function loadAlerts() {
    try {
        const response = await fetch(`${API_BASE}/alerts`);
        const alerts = await response.json();
        
        const tbody = document.getElementById('alertsTableBody');
        tbody.innerHTML = '';
        
        alerts.forEach(alert => {
            const student = studentsMap[alert.student_id];
            const studentName = student ? `${student.first_name} ${student.last_name}` : 'Unknown';
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(alert.sent_at)}</td>
                <td>${studentName}</td>
                <td>${alert.alert_type}</td>
                <td><span class="badge badge-${alert.severity}">${alert.severity.toUpperCase()}</span></td>
                <td>${alert.message}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading alerts:', error);
    }
}

// Load attendance
async function loadAttendance() {
    try {
        const response = await fetch(`${API_BASE}/attendance`);
        const records = await response.json();
        
        const tbody = document.getElementById('attendanceTableBody');
        tbody.innerHTML = '';
        
        records.slice(0, 50).forEach(record => {
            const student = studentsMap[record.student_id];
            const studentName = student ? `${student.first_name} ${student.last_name}` : 'Unknown';
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(record.date)}</td>
                <td>${studentName}</td>
                <td><span class="badge badge-${record.status}">${record.status.toUpperCase()}</span></td>
                <td>${record.notes || ''}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading attendance:', error);
    }
}

// Load grades
async function loadGrades() {
    try {
        const response = await fetch(`${API_BASE}/grades`);
        const grades = await response.json();
        
        const tbody = document.getElementById('gradesTableBody');
        tbody.innerHTML = '';
        
        grades.slice(0, 50).forEach(grade => {
            const student = studentsMap[grade.student_id];
            const studentName = student ? `${student.first_name} ${student.last_name}` : 'Unknown';
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(grade.date)}</td>
                <td>${studentName}</td>
                <td>${grade.subject}</td>
                <td>${grade.assignment_name}</td>
                <td>${grade.score}/${grade.max_score}</td>
                <td style="color: ${grade.percentage < 70 ? 'red' : 'green'}; font-weight: bold;">${grade.percentage}%</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading grades:', error);
    }
}

// Load behaviors
async function loadBehaviors() {
    try {
        const response = await fetch(`${API_BASE}/behaviors`);
        const behaviors = await response.json();
        
        const tbody = document.getElementById('behaviorsTableBody');
        tbody.innerHTML = '';
        
        behaviors.slice(0, 50).forEach(behavior => {
            const student = studentsMap[behavior.student_id];
            const studentName = student ? `${student.first_name} ${student.last_name}` : 'Unknown';
            
            const row = document.createElement('tr');
            row.innerHTML = `
                <td>${formatDate(behavior.date)}</td>
                <td>${studentName}</td>
                <td>${behavior.incident_type.replace('_', ' ')}</td>
                <td><span class="badge badge-${behavior.severity}">${behavior.severity.toUpperCase()}</span></td>
                <td>${behavior.description || ''}</td>
            `;
            tbody.appendChild(row);
        });
    } catch (error) {
        console.error('Error loading behaviors:', error);
    }
}

// View student details
async function viewStudent(studentId) {
    try {
        const response = await fetch(`${API_BASE}/students/${studentId}/dashboard`);
        const data = await response.json();
        
        const student = data.student;
        
        let html = `
            <div class="student-detail">
                <h2>${student.first_name} ${student.last_name}</h2>
                
                <div class="detail-section">
                    <h3>Student Information</h3>
                    <div class="info-grid">
                        <div class="info-item">
                            <label>Student ID:</label>
                            <value>${student.student_id}</value>
                        </div>
                        <div class="info-item">
                            <label>Grade Level:</label>
                            <value>${student.grade_level || 'N/A'}</value>
                        </div>
                        <div class="info-item">
                            <label>Special Education:</label>
                            <value>${student.special_ed ? 'Yes' : 'No'}</value>
                        </div>
                    </div>
                    ${student.accommodations ? `<div class="info-item"><label>Accommodations:</label><value>${student.accommodations}</value></div>` : ''}
                </div>
                
                <div class="detail-section">
                    <h3>Contacts</h3>
                    ${data.contacts.length > 0 ? `
                        <table>
                            <thead>
                                <tr>
                                    <th>Name</th>
                                    <th>Relationship</th>
                                    <th>Email</th>
                                    <th>Phone</th>
                                    <th>Alerts</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.contacts.map(c => `
                                    <tr>
                                        <td>${c.name}</td>
                                        <td>${c.relationship}</td>
                                        <td>${c.email || 'N/A'}</td>
                                        <td>${c.phone || 'N/A'}</td>
                                        <td>${c.receive_alerts ? '✓' : ''}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    ` : '<p>No contacts added yet.</p>'}
                </div>
                
                <div class="detail-section">
                    <h3>Recent Alerts</h3>
                    ${data.alerts.length > 0 ? `
                        <table>
                            <thead>
                                <tr>
                                    <th>Date</th>
                                    <th>Type</th>
                                    <th>Severity</th>
                                    <th>Message</th>
                                </tr>
                            </thead>
                            <tbody>
                                ${data.alerts.map(a => `
                                    <tr>
                                        <td>${formatDate(a.sent_at)}</td>
                                        <td>${a.alert_type}</td>
                                        <td><span class="badge badge-${a.severity}">${a.severity.toUpperCase()}</span></td>
                                        <td>${a.message}</td>
                                    </tr>
                                `).join('')}
                            </tbody>
                        </table>
                    ` : '<p>No alerts for this student.</p>'}
                </div>
            </div>
        `;
        
        document.getElementById('studentDetailContent').innerHTML = html;
        document.getElementById('studentDetailModal').style.display = 'block';
    } catch (error) {
        console.error('Error loading student details:', error);
        showMessage('Error loading student details', 'error');
    }
}

// Add student
async function addStudent(event) {
    event.preventDefault();
    
    const form = event.target;
    const formData = new FormData(form);
    
    const studentData = {
        first_name: formData.get('first_name'),
        last_name: formData.get('last_name'),
        student_id: formData.get('student_id'),
        grade_level: formData.get('grade_level') ? parseInt(formData.get('grade_level')) : null,
        special_ed: formData.get('special_ed') === 'on',
        accommodations: formData.get('accommodations')
    };
    
    try {
        const response = await fetch(`${API_BASE}/students`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(studentData)
        });
        
        if (response.ok) {
            showMessage('Student added successfully', 'success');
            closeModal('addStudentModal');
            form.reset();
            loadDashboard();
        } else {
            showMessage('Error adding student', 'error');
        }
    } catch (error) {
        console.error('Error adding student:', error);
        showMessage('Error adding student', 'error');
    }
}

// Check alerts
async function checkAlerts() {
    try {
        showMessage('Running alert checks...', 'success');
        const response = await fetch(`${API_BASE}/alerts/check`, {
            method: 'POST'
        });
        const data = await response.json();
        showMessage(data.message, 'success');
        loadDashboard();
    } catch (error) {
        console.error('Error checking alerts:', error);
        showMessage('Error checking alerts', 'error');
    }
}

// Tab switching
function showTab(tabName) {
    // Hide all tabs
    document.querySelectorAll('.tab-content').forEach(tab => {
        tab.classList.remove('active');
    });
    
    // Remove active class from all buttons
    document.querySelectorAll('.tab-btn').forEach(btn => {
        btn.classList.remove('active');
    });
    
    // Show selected tab
    document.getElementById(tabName + 'Tab').classList.add('active');
    
    // Add active class to clicked button
    event.target.classList.add('active');
}

// Modal functions
function showAddStudentModal() {
    document.getElementById('addStudentModal').style.display = 'block';
}

function closeModal(modalId) {
    document.getElementById(modalId).style.display = 'none';
}

// Close modal when clicking outside
window.onclick = function(event) {
    if (event.target.classList.contains('modal')) {
        event.target.style.display = 'none';
    }
}

// Utility functions
function formatDate(dateString) {
    if (!dateString) return 'N/A';
    const date = new Date(dateString);
    return date.toLocaleDateString('en-US', { year: 'numeric', month: 'short', day: 'numeric' });
}

function showMessage(message, type) {
    // Remove existing messages
    document.querySelectorAll('.message').forEach(msg => msg.remove());
    
    const messageDiv = document.createElement('div');
    messageDiv.className = `message ${type}`;
    messageDiv.textContent = message;
    
    document.querySelector('.container').insertBefore(messageDiv, document.querySelector('header').nextSibling);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        messageDiv.remove();
    }, 5000);
}
