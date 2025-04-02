from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()

class User(Base):
    __tablename__ = 'users'
    id = Column(Integer, primary_key=True, autoincrement=True)
    username = Column(String(50), nullable=False, unique=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    created_at = Column(DateTime, nullable=False)

class Test(Base):
    __tablename__ = 'tests'
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_by = Column(Integer, ForeignKey('users.id'), nullable=False)
    created_at = Column(DateTime, nullable=False)
    user = relationship("User", back_populates="tests")

class TestCase(Base):
    __tablename__ = 'testcases'
    id = Column(Integer, primary_key=True, autoincrement=True)
    test_id = Column(Integer, ForeignKey('tests.id'), nullable=False)
    name = Column(String(100), nullable=False)
    description = Column(Text, nullable=True)
    created_at = Column(DateTime, nullable=False)
    test = relationship("Test", back_populates="testcases")

class Result(Base):
    __tablename__ = 'results'
    id = Column(Integer, primary_key=True, autoincrement=True)
    testcase_id = Column(Integer, ForeignKey('testcases.id'), nullable=False)
    status = Column(String(50), nullable=False)  # e.g., 'passed', 'failed'
    executed_at = Column(DateTime, nullable=False)
    testcase = relationship("TestCase", back_populates="results")

# Relationships
User.tests = relationship("Test", order_by=Test.id, back_populates="user")
Test.testcases = relationship("TestCase", order_by=TestCase.id, back_populates="test")
TestCase.results = relationship("Result", order_by=Result.id, back_populates="testcase")
