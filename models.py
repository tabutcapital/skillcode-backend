from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(50), nullable=False, unique=True)
    email = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    tests = db.relationship("Test", back_populates="user")

class Test(db.Model):
    __tablename__ = 'tests'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_by = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)
    user = db.relationship("User", back_populates="tests")
    testcases = db.relationship("TestCase", back_populates="test")

class TestCase(db.Model):
    __tablename__ = 'testcases'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    test_id = db.Column(db.Integer, db.ForeignKey('tests.id'), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    created_at = db.Column(db.DateTime, nullable=False)
    test = db.relationship("Test", back_populates="testcases")

class Result(db.Model):
    __tablename__ = 'results'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    testcase_id = db.Column(db.Integer, db.ForeignKey('testcases.id'), nullable=False)
    status = db.Column(db.String(50), nullable=False)  # e.g., 'passed', 'failed'
    executed_at = db.Column(db.DateTime, nullable=False)
    testcase = db.relationship("TestCase", back_populates="results")

# Relationships
TestCase.results = db.relationship("Result", order_by=Result.id, back_populates="testcase")
