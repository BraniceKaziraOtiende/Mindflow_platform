from flask import Flask, render_template, request, redirect, url_for
from sqlalchemy import create_engine, Column, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)

# Configure MySQL database connection
DATABASE_URI = 'mysql+pymysql://username:password@localhost/learners_registration'
engine = create_engine(DATABASE_URI)
Base = declarative_base()

# Define the Names table
class Name(Base):
    __tablename__ = 'names'
    id = Column(String(50), primary_key=True)  # Use email or any unique identifier
    email = Column(String(100), unique=True)

# Define the Passwords table
class Password(Base):
    __tablename__ = 'passwords'
    id = Column(String(50), ForeignKey('names.id'), primary_key=True)
    password_hash = Column(String(255))

    # Set up a relationship with the Names table
    user = relationship("Name", backref="password_entry")

Base.metadata.create_all(engine)  # Create the tables if they don't exist

# Set up a session
Session = sessionmaker(bind=engine)
session = Session()

@app.route('/')
def home():
    return render_template('login.html')  # Render the login/registration form

@app.route('/process', methods=['POST'])
def process():
    action = request.form['action']
    email = request.form['email']
    password = request.form['password']

    if action == "register":
        # Check if the user already exists in the Names table
        existing_user = session.query(Name).filter_by(email=email).first()
        if existing_user:
            return f"User with email {email} already exists!"

        # Hash the password
        hashed_password = generate_password_hash(password)

        # Add new user to the database in both tables
        new_user = Name(id=email, email=email)  # Use email as ID
        new_password_entry = Password(id=email, password_hash=hashed_password)
        
        session.add(new_user)
        session.add(new_password_entry)
        session.commit()

        return f"Registration successful for {email}"

    elif action == "login":
        # Check if the user exists in the Names table
        user = session.query(Name).filter_by(email=email).first()
        if user:
            # Get the password entry from the Passwords table
            password_entry = session.query(Password).filter_by(id=user.id).first()
            if password_entry and check_password_hash(password_entry.password_hash, password):
                return f"Login successful for {email}"
            else:
                return "Invalid email or password."
    
    return redirect(url_for('home'))

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)

