
from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import time
import math
from smart_university_id_system import HashTable, Trie, LogQueue, Graph, Student

app = Flask(__name__)
app.secret_key = 'smart_university_secret_key_2024'  # For flash messages

# Initialize backend systems
students = HashTable()
trie = Trie()
logs = LogQueue()
graph = Graph()


def load_example_data():
    """Load example test data for demonstration."""
    # Add 5 students
    demo_students = [
        (101, "Awais Khan", "CS", "2025"),
        (102, "Alice Johnson", "Math", "2024"),
        (103, "Ahmad Raza", "EE", "2026"),
        (104, "Karen Smith", "Physics", "2023"),
        (105, "Khalid Hussain", "CS", "2025"),
    ]
    
    for sid, name, dept, batch in demo_students:
        students.insert_student(sid, name, dept, batch)
        trie.insert(name)
    
    # Add 5 logs with different timestamps
    base_time = time.time() - 3600  # 1 hour ago
    demo_logs = [
        (101, "Library", base_time),
        (102, "Cafeteria", base_time + 600),
        (103, "Main Gate", base_time + 1200),
        (104, "Lab A", base_time + 1800),
        (105, "Auditorium", base_time + 2400),
    ]
    
    for log in demo_logs:
        logs.enqueue(log)
    
    # Add 4 blocks and paths
    blocks = ["Main Gate", "Library", "Cafeteria", "Lab A"]
    for b in blocks:
        graph.add_block(b)
    
    graph.add_path("Main Gate", "Library", 5.0)
    graph.add_path("Library", "Cafeteria", 3.0)
    graph.add_path("Cafeteria", "Lab A", 4.0)
    graph.add_path("Main Gate", "Lab A", 12.0)


# Load example data on startup
load_example_data()


@app.route('/')
def index():
    """Home / Dashboard page."""
    return render_template('index.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    """Add Student page."""
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id', '').strip())
            name = request.form.get('name', '').strip()
            department = request.form.get('department', '').strip()
            batch = request.form.get('batch', '').strip()
            
            if not name or not department or not batch:
                flash('All fields are required!', 'error')
                return render_template('add_student.html')
            
            if students.insert_student(student_id, name, department, batch):
                trie.insert(name)
                flash(f'Student {name} (ID: {student_id}) added successfully!', 'success')
                return redirect(url_for('add_student'))
            else:
                flash('Duplicate ID detected! Student ID already exists.', 'error')
                return render_template('add_student.html')
        except ValueError:
            flash('Invalid Student ID! Please enter a valid number.', 'error')
            return render_template('add_student.html')
    
    return render_template('add_student.html')


@app.route('/verify_student', methods=['GET', 'POST'])
def verify_student():
    """Verify Student ID page."""
    result = None
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id', '').strip())
            student = students.search_student(student_id)
            
            if student:
                result = {
                    'status': 'valid',
                    'message': 'Valid ID',
                    'student': {
                        'id': student.id,
                        'name': student.name,
                        'department': student.department,
                        'batch': student.batch
                    }
                }
            else:
                result = {
                    'status': 'invalid',
                    'message': 'Invalid or Fake ID'
                }
        except ValueError:
            result = {
                'status': 'error',
                'message': 'Invalid Input - Please enter a valid Student ID number.'
            }
    
    return render_template('verify_student.html', result=result)


@app.route('/search_name', methods=['GET', 'POST'])
def search_name():
    """Search Student by Name page."""
    suggestions = []
    prefix = ''
    if request.method == 'POST':
        prefix = request.form.get('prefix', '').strip()
        if prefix:
            suggestions = trie.get_suggestions(prefix)
    
    return render_template('search_name.html', suggestions=suggestions, prefix=prefix)


@app.route('/log_entry', methods=['GET', 'POST'])
def log_entry():
    """Log Entry page."""
    if request.method == 'POST':
        try:
            student_id = int(request.form.get('student_id', '').strip())
            location = request.form.get('location', '').strip()
            
            if not location:
                flash('Location is required!', 'error')
                return render_template('log_entry.html')
            
            # Verify student exists
            if not students.search_student(student_id):
                flash(f'Student ID {student_id} not found in system!', 'error')
                return render_template('log_entry.html')
            
            timestamp = time.time()
            logs.enqueue((student_id, location, timestamp))
            
            formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(timestamp))
            flash(f'Entry logged successfully! Student ID: {student_id}, Location: {location}, Time: {formatted_time}', 'success')
            return redirect(url_for('log_entry'))
        except ValueError:
            flash('Invalid Student ID! Please enter a valid number.', 'error')
            return render_template('log_entry.html')
    
    return render_template('log_entry.html')


@app.route('/show_logs')
def show_logs():
    """Show Entry Logs page."""
    all_logs = logs.display_logs()
    # Format timestamps for display
    formatted_logs = []
    for sid, location, ts in all_logs:
        formatted_time = time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(ts))
        formatted_logs.append({
            'student_id': sid,
            'location': location,
            'timestamp': formatted_time
        })
    return render_template('show_logs.html', logs=formatted_logs)


@app.route('/shortest_path', methods=['GET', 'POST'])
def shortest_path():
    """Shortest Path Between Blocks page."""
    result = None
    available_blocks = list(graph.adj.keys())
    
    if request.method == 'POST':
        start = request.form.get('start_block', '').strip()
        end = request.form.get('end_block', '').strip()
        
        if not start or not end:
            result = {
                'status': 'error',
                'message': 'Please enter both start and end blocks.'
            }
        else:
            dist, path = graph.shortest_path(start, end)
            if math.isinf(dist):
                result = {
                    'status': 'no_path',
                    'message': f'No path found between "{start}" and "{end}".',
                    'available_blocks': available_blocks
                }
            else:
                result = {
                    'status': 'success',
                    'distance': dist,
                    'path': path,
                    'path_str': ' → '.join(path)
                }
    
    return render_template('shortest_path.html', result=result, available_blocks=available_blocks)


if __name__ == '__main__':
    print("\n" + "="*60)
    print("Smart University ID & Verification System")
    print("="*60)
    print("\nStarting Flask server...")
    print("Open your browser and navigate to: http://127.0.0.1:5000")
    print("\nPress CTRL+C to stop the server.")
    print("="*60 + "\n")
    app.run(debug=True, host='127.0.0.1', port=5000)
