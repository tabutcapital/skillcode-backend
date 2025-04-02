from flask import Blueprint, request, jsonify
from app import db
from models import TestCase

results_bp = Blueprint('results', __name__)

@results_bp.route('/evaluate', methods=['POST'])
def evaluate_code():
    data = request.get_json()
    code = data['code']
    test_id = data['test_id']

    # This is a simple example. In production, you'd run the code in a sandboxed environment.
    # For now, we'll just mock the evaluation by checking the code against test cases.
    test_cases = TestCase.query.filter_by(test_id=test_id).all()
    results = []

    for test_case in test_cases:
        # Here you can use a library like exec to run the student's code and compare with expected output.
        # For now, we just simulate this check.
        if code == test_case.expected_output:
            results.append({"test_case_id": test_case.id, "passed": True})
        else:
            results.append({"test_case_id": test_case.id, "passed": False})

    return jsonify(results=results), 200
