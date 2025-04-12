import os
from flask import Flask, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
from flask_socketio import SocketIO
from dotenv import load_dotenv
from datetime import datetime

# Load environment variables
load_dotenv()

# Initialize extensions
db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def create_app(config_name='default'):
    """Create and configure the Flask application"""
    app = Flask(__name__)

    # Load configuration
    from app.config import config
    app.config.from_object(config[config_name])

    # Initialize extensions with the app
    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = 'auth.login'
    socketio.init_app(app, cors_allowed_origins="*")

    # Register blueprints
    from app.routes.auth import auth as auth_blueprint
    app.register_blueprint(auth_blueprint)

    from app.routes.users import users as users_blueprint
    app.register_blueprint(users_blueprint)

    from app.routes.channels import channels as channels_blueprint
    app.register_blueprint(channels_blueprint)

    from app.routes.messages import messages as messages_blueprint
    app.register_blueprint(messages_blueprint)

    # Add context processor for templates
    @app.context_processor
    def inject_now():
        return {'now': datetime.utcnow()}

    # Add error handler for 500 errors
    @app.errorhandler(500)
    def internal_error(error):
        app.logger.error(f"Server Error: {error}")
        return render_template('error.html', error=error), 500

    # Root route
    @app.route('/')
    def index():
        return render_template('index.html')

    # Create database tables if they don't exist
    with app.app_context():
        db.create_all()

    return app