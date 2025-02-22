from flask import Flask, render_template, request, redirect, url_for, jsonify
import json

app = Flask(__name__)

# JSON file for storing student data
STUDENT_FILE = "students.json"

def load_students():
    try:
        with open(STUDENT_FILE, "r") as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []

def save_students(students):
    with open(STUDENT_FILE, "w") as f:
        json.dump(students, f, indent=4)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/students')
def student_list():
    students = load_students()
    return render_template('students.html', students=students)

@app.route('/add', methods=['POST'])
def add_student():
    name = request.form['name']
    email = request.form['email']
    age = request.form['age']

    students = load_students()
    students.append({"name": name, "email": email, "age": age})
    save_students(students)

    return redirect(url_for('student_list'))

@app.route('/delete/<email>')
def delete_student(email):
    students = load_students()
    students = [s for s in students if s['email'] != email]
    save_students(students)
    return redirect(url_for('student_list'))

@app.route('/update/<email>', methods=['GET', 'POST'])
def update_student(email):
    students = load_students()
    student = next((s for s in students if s['email'] == email), None)

    if request.method == 'POST':
        student['name'] = request.form['name']
        student['age'] = request.form['age']
        save_students(students)
        return redirect(url_for('student_list'))

    return render_template('update_student.html', student=student)

if __name__ == '__main__':
    app.run(debug=True)
