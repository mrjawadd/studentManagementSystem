from flask import Flask, render_template, request, redirect, url_for
import sqlite3

app = Flask(__name__)

# --- Database Setup ---
def init_db():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    # Create students table
    cursor.execute('''CREATE TABLE IF NOT EXISTS students (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL,
                        course TEXT NOT NULL
                    )''')

    # Create courses table
    cursor.execute('''CREATE TABLE IF NOT EXISTS courses (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        name TEXT NOT NULL UNIQUE
                    )''')

    # Add default courses
    default_courses = [
        ('Python Development',),
        ('Mobile Development',),
        ('Digital Marketing',),
        ('Graphic Designing',),
        ('Web Development',),
        ('UI/UX Design',),
        ('Data Science',)
    ]
    cursor.executemany('INSERT OR IGNORE INTO courses (name) VALUES (?)', default_courses)

    conn.commit()
    conn.close()


# Initialize DB on app start
init_db()


# --- Routes ---
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/add_student', methods=['GET', 'POST'])
def add_student():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()

    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']

        cursor.execute("INSERT INTO students (name, course) VALUES (?, ?)", (name, course))
        conn.commit()
        conn.close()
        return redirect(url_for('view_students'))

    conn.close()
    return render_template('add_student.html', courses=courses)


@app.route('/view_students')
def view_students():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM students")
    students = cursor.fetchall()
    conn.close()
    return render_template('view_students.html', students=students)


@app.route('/delete_student/<int:id>')
def delete_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM students WHERE id = ?", (id,))
    conn.commit()
    conn.close()
    return redirect(url_for('view_students'))


@app.route('/edit_student/<int:id>', methods=['GET', 'POST'])
def edit_student(id):
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()

    if request.method == 'POST':
        name = request.form['name']
        course = request.form['course']
        cursor.execute("UPDATE students SET name = ?, course = ? WHERE id = ?", (name, course, id))
        conn.commit()
        conn.close()
        return redirect(url_for('view_students'))

    else:
        cursor.execute("SELECT * FROM students WHERE id = ?", (id,))
        student = cursor.fetchone()
        cursor.execute("SELECT * FROM courses")
        courses = cursor.fetchall()
        conn.close()
        return render_template('edit_student.html', student=student, courses=courses)



@app.route('/view_courses')
def view_courses():
    conn = sqlite3.connect('database.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM courses")
    courses = cursor.fetchall()
    conn.close()
    return render_template('view_courses.html', courses=courses)


if __name__ == '__main__':
    app.run(debug=True)
