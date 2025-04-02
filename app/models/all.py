from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin

db = SQLAlchemy()

# User Model for Technical Mentor and Student
class User(db.Model, UserMixin):  # Inherit from UserMixin to add required properties
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(200), nullable=False)
    role = db.Column(db.String(20), nullable=False)
    tests = db.relationship('Test', backref='creator', lazy=True)
    results = db.relationship('Result', backref='student', lazy=True)

    # UserMixin provides the following properties:
    # - is_authenticated
    # - is_active
    # - is_anonymous
    # - get_id
    # No additional implementation is needed unless you want to customize behavior.

    def __repr__(self):
        return f'<User {self.username}>'

# Test Model (created by TM)
class Test(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    results = db.relationship('Result', backref='test', lazy=True)

# Result Model (linked to Test and Student)
class Result(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    score = db.Column(db.Integer, nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)

class TestCase(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.Integer, db.ForeignKey('test.id'), nullable=False)
    input_data = db.Column(db.String(500), nullable=False)
    expected_output = db.Column(db.String(500), nullable=False)

    test = db.relationship('Test', back_populates="test_cases")

Test.test_cases = db.relationship('TestCase', back_populates="test", lazy=True)
