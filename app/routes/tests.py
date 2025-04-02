from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Test, TestCase

tests_bp = Blueprint('tests', __name__)

@tests_bp.route('/create', methods=['POST'])
@login_required
def create_test():
    if current_user.role != 'TM':
        return jsonify(message="Unauthorized access"), 403

    data = request.get_json()
    name = data['name']
    description = data['description']
    questions = data['questions']  # Array of questions with inputs and outputs

    new_test = Test(name=name, description=description, created_by=current_user.id)
    db.session.add(new_test)
    db.session.commit()

    # Create test cases for each question
    for question in questions:
        for test_case in question.test_cases:
            new_test_case = TestCase(
                test_id=new_test.id,
                input_data=test_case.input_data,
                expected_output=test_case.expected_output
            )
            db.session.add(new_test_case)

    db.session.commit()
    return jsonify(message="Test created successfully"), 201
