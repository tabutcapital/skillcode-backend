from flask import Blueprint, request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from app.models.all import db, User, Test, TestCase, Result

routes = Blueprint('routes', __name__)

# Signup route
@routes.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    hashed_password = generate_password_hash(data['password'])
    new_user = User(username=data['username'], password=hashed_password, role=data['role'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify({"message": "User created successfully!"}), 201

# Login route
@routes.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    user = User.query.filter_by(username=data['username']).first()
    if user and check_password_hash(user.password, data['password']):
        return jsonify({"message": "Login successful!", "role": user.role}), 200
    return jsonify({"message": "Invalid username or password"}), 401

# CRUD for Test
@routes.route('/tests', methods=['POST'])
def create_test():
    data = request.get_json()
    new_test = Test(name=data['name'], description=data['description'], created_by=data['created_by'])
    db.session.add(new_test)
    db.session.commit()
    return jsonify({"message": "Test created successfully!"}), 201

@routes.route('/tests', methods=['GET'])
def get_tests():
    tests = Test.query.all()
    return jsonify([{"id": test.id, "name": test.name, "description": test.description} for test in tests]), 200

# CRUD for TestCase
@routes.route('/testcases', methods=['POST'])
def create_testcase():
    data = request.get_json()
    new_testcase = TestCase(test_id=data['test_id'], input_data=data['input_data'], expected_output=data['expected_output'])
    db.session.add(new_testcase)
    db.session.commit()
    return jsonify({"message": "TestCase created successfully!"}), 201

@routes.route('/testcases', methods=['GET'])
def get_testcases():
    testcases = TestCase.query.all()
    return jsonify([{"id": tc.id, "test_id": tc.test_id, "input_data": tc.input_data, "expected_output": tc.expected_output} for tc in testcases]), 200

# CRUD for Result
@routes.route('/results', methods=['POST'])
def create_result():
    data = request.get_json()
    new_result = Result(score=data['score'], student_id=data['student_id'], test_id=data['test_id'])
    db.session.add(new_result)
    db.session.commit()
    return jsonify({"message": "Result created successfully!"}), 201

@routes.route('/results', methods=['GET'])
def get_results():
    results = Result.query.all()
    return jsonify([{"id": res.id, "score": res.score, "student_id": res.student_id, "test_id": res.test_id} for res in results]), 200
