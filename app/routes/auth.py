from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from datetime import datetime, timedelta
# from app.models import db
# from models import User
from app.models.all import User
from app import db

auth_bp = Blueprint('auth', __name__)

SECRET_KEY = "your_secret_key"  # Replace with a secure key

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()

    # Validate input data
    if not data or 'first_name' not in data or 'email' not in data or 'password' not in data or 'role' not in data:
        return jsonify(message="Missing required fields: 'first_name', 'email', 'password', or 'role'"), 400

    first_name = data['first_name']
    email = data['email']
    password = generate_password_hash(data['password'])
    role = data['role']  # 'TM' or 'Student'

    # Check if the email already exists
    if User.query.filter_by(email=email).first():
        return jsonify(message="Email already exists"), 409

    new_user = User(first_name=first_name, email=email, password=password, role=role)

    try:
        db.session.add(new_user)
        db.session.commit()
        return jsonify(message="User created successfully"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(message="Error creating user", error=str(e)), 500

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    email = data['email']
    password = data['password']

    user = User.query.filter_by(email=email).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        
        # Generate JWT token
        token = jwt.encode({
            'user_id': user.id,
            'exp': datetime.utcnow() + timedelta(hours=24)
        }, SECRET_KEY, algorithm='HS256')

        return jsonify(message="Login successful", role=user.role, token=token), 200
    return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message="Logged out successfully"), 200
