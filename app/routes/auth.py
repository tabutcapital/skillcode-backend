from flask import Blueprint, request, jsonify
from flask_login import login_user, logout_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
# from app.models import db
# from models import User
from app.models.models import User
from app import db

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    username = data['username']
    password = generate_password_hash(data['password'])
    role = data['role']  # 'TM' or 'Student'

    new_user = User(username=username, password=password, role=role)

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
    username = data['username']
    password = data['password']

    user = User.query.filter_by(username=username).first()
    if user and check_password_hash(user.password, password):
        login_user(user)
        return jsonify(message="Login successful", role=user.role), 200
    return jsonify(message="Invalid credentials"), 401

@auth_bp.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify(message="Logged out successfully"), 200
