from flask import Flask, render_template, request, redirect, url_for,send_file
from werkzeug.utils import secure_filename
from flask import Flask, render_template, request, redirect, url_for, flash, session, jsonify
from flask_login import LoginManager, UserMixin, login_user, logout_user, current_user, login_required
import numpy as np
from werkzeug.security import generate_password_hash, check_password_hash
from create_database import create_connection, create_table, create_table2
from flask_socketio import SocketIO, emit
import pdfkit
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
from flask_socketio import SocketIO, emit, join_room, leave_room


students_connected = -1


app = Flask(__name__)
app.secret_key = '123456789'  # Required for session management
socketio = SocketIO(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'signin'

class User(UserMixin):
    def __init__(self, id, name, email):
        self.id = id
        self.name = name
        self.email = email


create_table()
create_table2()


@app.route('/', methods=['POST', 'GET'])
def index():
    if request.method == 'POST':
        name = request.form['Username']
        email = request.form['Email']
        password = request.form['Password2']

        # Check if any of the fields are empty
        if not name or not email or not password:
            fill_error = "All fields are required"
            return render_template('login.html', fill_error=fill_error)
        else:
            pass

        conn = create_connection()
        c = conn.cursor()

        # Check if the user already exists
        c.execute('SELECT * FROM students WHERE name = ?', (name,))
        existing_user = c.fetchone()

        if existing_user:
            error = "User already exists"
            conn.close()
            return render_template('login.html', error=error)
        else:
            # Hash the password and insert the new user into the database
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            c.execute('''INSERT INTO students (name, email, password) 
                         VALUES (?, ?, ?)''', (name, email, hashed_password))
            conn.commit()
            conn.close()

            return redirect(url_for('student'))

    return render_template('login.html')

@app.route('/instructor', methods=['POST', 'GET'])
def instructor():
    if request.method == 'POST':
        name = request.form['Username']
        email = request.form['Email']
        password = request.form['Password2']

        # Check if any of the fields are empty
        if not name or not email or not password:
            fill_error = "All fields are required"
            return render_template('login.html', fill_error=fill_error)
        else:
            pass

        conn = create_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM instructors WHERE name = ?', (name,))
        existing_user = c.fetchone()

        if existing_user:
            error = "User already exists"
            conn.close()
            return render_template('login_instructor.html', error=error)
        else:
            hashed_password = generate_password_hash(password, method='pbkdf2:sha256')
            c.execute('''INSERT INTO instructors (name, email, password) 
                         VALUES (?, ?, ?)''', (name, email, hashed_password))
            conn.commit()
            conn.close()

            return redirect(url_for('lecture'))

    return render_template('login_instructor.html')

@login_manager.user_loader
def load_user(user_id):
    conn = create_connection()
    c = conn.cursor()
    c.execute('SELECT * FROM students WHERE id = ?', (user_id,))
    user = c.fetchone()
    conn.close()
    if user:
        return User(id=user[0], name=user[1], email=user[2])
    return None

@app.route('/signin', methods=['POST', 'GET'])
def signin():
    if request.method == 'POST':
        name = request.form['Username']
        password = request.form['Password2']

        # Check if any of the fields are empty
        if not name or not password:
            fill_error = "All fields are required"
            return render_template('login.html', fill_error=fill_error)
        else:
            pass

        print(name, password)

        conn = create_connection()
        c = conn.cursor()

        c.execute('SELECT * FROM students WHERE name = ?', (name,))
        user = c.fetchone()
        conn.close()
        print(user[3])

        if user and check_password_hash(user[3], password):
            user_obj = User(id=user[0], name=user[1], email=user[2])
            login_user(user_obj)
            return redirect(url_for('student'))
        else:
            error = "Invalid username or password"
            return render_template('signin.html', error=error)

    return render_template('signin.html')

transcription = ""

@app.route('/lecture')
def lecture():
    return render_template('instructor.html')

@app.route('/student')
def student():
    return render_template('student.html')

@socketio.on('transcribe')
def handle_transcribe(data):
    global transcription
    transcription += data['text']
    emit('update_transcription', {'text': transcription}, broadcast=True)



@socketio.on('connect')
def handle_connect():
    global students_connected
    students_connected += 1
    emit('update_student_count', students_connected, broadcast=True)

@socketio.on('disconnect')
def handle_disconnect():
    global students_connected
    students_connected -= 1
    emit('update_student_count', students_connected, broadcast=True)

@app.route('/download')
def download():
    global transcription
    pdf_buffer = BytesIO()
    c = canvas.Canvas(pdf_buffer, pagesize=letter)
    c.drawString(100, 750, "Transcription:")
    lines = transcription.split('\n')
    y = 730
    for line in lines:
        c.drawString(100, y, line)
        y -= 15
    c.showPage()
    c.save()
    pdf_buffer.seek(0)
    return send_file(pdf_buffer, as_attachment=True, download_name='transcription.pdf', mimetype='application/pdf')


if __name__ == '__main__':
    socketio.run(app, debug=True)
