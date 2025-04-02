from flask_sqlalchemy import SQLAlchemy
db = SQLAlchemy()

from .all import User, Test, Result, TestCase  # Import all models here

__all__ = ["User", "Test", "Result", "TestCase"]
