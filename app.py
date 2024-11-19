from flask import Flask, render_template, request, redirect, url_for
import mysql.connector
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure the MySQL connection
db_config = {
    'host': 'localhost',  
    'user': 'maureen',  
    'password': 'mypassword', 
    'database': 'student_credentials' 
}

# Create a connection to the database
def get_db_connection():
    return mysql.connector.connect(**db_config)

@app.route('/')
def home():
    return render_template('login.html')  # Render the login/registration form

@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    email = request.form['email']
    password = request.form['password']
    
    connection = get_db_connection()
    cursor = connection.cursor()

    if action == "register":
        # Check if the user already exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        existing_user = cursor.fetchone()
        
        if existing_user:
            return f"User with email {email} already exists!"
        
        # Hash the password for security
        hashed_password = generate_password_hash(password)
        
        # Insert the new user into the database
        cursor.execute("INSERT INTO users (email, password) VALUES (%s, %s)", (email, hashed_password))
        connection.commit()
        
        return f"Registration successful for {email}"

    elif action == "login":
        # Check if the user exists
        cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
        user = cursor.fetchone()

        if user and check_password_hash(user[1], password):  # user[1] is the password field
            return f"Login successful for {email}"
        else:
            return "Invalid email or password."

    connection.close()
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)

