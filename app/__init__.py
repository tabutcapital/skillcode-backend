from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from app.models.all import db, User  # Ensure this is the correct import
from app.routes import routes  # Ensure this import works after fixing the routes package
from app.routes.auth import auth_bp  # Import the auth blueprint
from app.routes.codeevaluation import results_bp  # Ensure this import works

migrate = Migrate()
login_manager = LoginManager()

def create_app():
    app = Flask(__name__)
    app.config.from_object('config.Config')  # Assuming you have a config class

    # Set a secret key for session management
    app.secret_key = 'your-secret-key'  # Replace 'your-secret-key' with a secure, random value

    # Initialize extensions
    db.init_app(app)  # Ensure db is initialized with the app
    migrate.init_app(app, db)
    login_manager.init_app(app)

    # Configure the user loader
    @login_manager.user_loader
    def load_user(user_id):
        return User.query.get(int(user_id))

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(routes, url_prefix='/')
    app.register_blueprint(results_bp)

    return app
