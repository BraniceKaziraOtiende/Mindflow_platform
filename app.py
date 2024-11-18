from flask import Flask, request, render_template, redirect, url_for, flash
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Needed for flash messages

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host="localhost",
        user="maureen",
        password="mypassword",
        database="student_registration"
    )
    return connection

@app.route('/')
def index():
    return render_template('form.html')

@app.route('/submit', methods=['POST'])
def submit():
    email = request.form['email']
    password = request.form['password']
    action = request.form['action']

    connection = get_db_connection()
    cursor = connection.cursor(dictionary=True)

    if action == 'register':
        # Check if email already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user:
            flash("Account with this email already exists. Try logging in.")
        else:
            # Hash the password and insert new user into database
            hashed_password = generate_password_hash(password)
            cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
            connection.commit()
            flash("Account created successfully! Please log in.")

    elif action == 'login':
        # Check if email exists and verify password
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user['password'], password):
            flash("Login successful! Welcome back!")
        else:
            flash("Invalid email or password. Please try again.")

    cursor.close()
    connection.close()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5000)
