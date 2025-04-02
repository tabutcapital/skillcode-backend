from flask import Blueprint, request, jsonify
from flask_login import login_required, current_user
from app import db
from models import Result, Test

results_bp = Blueprint('results', __name__)

@results_bp.route('/submit', methods=['POST'])
@login_required
def submit_result():
    if current_user.role != 'Student':
        return jsonify(message="Unauthorized access"), 403

    data = request.get_json()
    test_id = data['test_id']
    score = data['score']

    new_result = Result(score=score, student_id=current_user.id, test_id=test_id)

    try:
        db.session.add(new_result)
        db.session.commit()
        return jsonify(message="Result submitted successfully"), 201
    except Exception as e:
        db.session.rollback()
        return jsonify(message="Error submitting result", error=str(e)), 500

@results_bp.route('/view', methods=['GET'])
@login_required
def view_results():
    results = Result.query.filter_by(student_id=current_user.id).all()
    return jsonify(results=[{"test_id": result.test_id, "score": result.score} for result in results]), 200
