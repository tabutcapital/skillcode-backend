from flask import Blueprint

routes = Blueprint('routes', __name__)

# Import all route modules to register their routes
from app.routes.auth import *  # Import the auth routes
from app.routes.main import *  # Import the main routes
from app.routes.tests import *  # Import the tests routes
from app.routes.results import *  # Import the results routes

