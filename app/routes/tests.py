from flask import Blueprint, request, jsonify
from app.models.all import db, Test

# Use the 'routes' blueprint instead of creating a new one
from app.routes import routes

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

@routes.route('/tests/<int:id>', methods=['GET'])
def get_test_by_id(id):
    test = Test.query.get(id)
    if not test:
        return jsonify({"error": "Test not found"}), 404
    return jsonify({"id": test.id, "name": test.name, "description": test.description}), 200
