from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)

# Connect to database
def connect_db():
    return sqlite3.connect('database.db')

# Create table if not exists
conn = connect_db()
conn.execute('''
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    email TEXT,
    course TEXT
)
''')
conn.close()

# HOME - Show all students
@app.route('/')
def index():
    conn = connect_db()
    students = conn.execute("SELECT * FROM students").fetchall()
    conn.close()
    return render_template('index.html', students=students)

# ADD student
@app.route('/add', methods=['GET', 'POST'])
def add():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn = connect_db()
        conn.execute(
            "INSERT INTO students (name, email, course) VALUES (?, ?, ?)",
            (name, email, course)
        )
        conn.commit()
        conn.close()

        return redirect('/')
    
    return render_template('add.html')

# EDIT student
@app.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit(id):
    conn = connect_db()

    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        course = request.form['course']

        conn.execute(
            "UPDATE students SET name=?, email=?, course=? WHERE id=?",
            (name, email, course, id)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    student = conn.execute(
        "SELECT * FROM students WHERE id=?", (id,)
    ).fetchone()
    conn.close()

    return render_template('edit.html', student=student)

# DELETE student
@app.route('/delete/<int:id>')
def delete(id):
    conn = connect_db()
    conn.execute("DELETE FROM students WHERE id=?", (id,))
    conn.commit()
    conn.close()

    return redirect('/')

# RUN APP
if __name__ == "__main__":
    app.run(debug=True)