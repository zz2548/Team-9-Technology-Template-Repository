from flask import Flask, jsonify, request, Response
from src.models import db
from src.models.channel_model import ChannelModel
from src.models.message_model import MessageModel
from src.models.user_model import UserModel
from src.models.channel_user_model import ChannelUserModel
from src.auth import generate_token, token_required, decode_token
from src.channel_impl.ai_bot_channel import AiBotChannel
import uuid
import logging
import os
import click
import datetime
from flask.cli import with_appcontext
from flask_cors import CORS
from flask_login import LoginManager, login_user, logout_user, login_required, \
    current_user
from dotenv import load_dotenv
from typing import Dict, List, Union, Optional, Any, Tuple, cast

# Load environment variables from .env file
load_dotenv()


def create_app() -> Flask:
    """
    Create and configure the Flask application.

    This function sets up the Flask application with all necessary configurations
    including database connection, CORS, environment variables, and feature flags.
    It also registers CLI commands for database management.

    Returns:
        Flask: The configured Flask application ready for use.
    """
    app = Flask(__name__)
    # Add supports_credentials for cookies
    # Configure CORS with support for credentials
    CORS(app,
         supports_credentials=True,
         resources={r"/*": {
             "origins": ["http://127.0.0.1:5000", "http://localhost:5000", "null"],
             "allow_headers": ["Content-Type", "Authorization", "X-Requested-With",
                               "Accept"],
             "expose_headers": ["Content-Type", "Authorization"],
             "methods": ["GET", "POST", "PUT", "DELETE", "OPTIONS"],
             "max_age": 86400
         }})

    # Database Configuration from environment variables
    db_type: str = os.getenv("DB_TYPE", "sqlite")
    db_path: str = os.getenv("DB_PATH", "chat.db")
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{db_type}:///{db_path}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS', 'False').lower() == 'true'

    # Server Configuration
    app.config['FLASK_ENV'] = os.getenv('FLASK_ENV', 'development')
    app.config['DEBUG'] = os.getenv('DEBUG', 'True').lower() == 'true'
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'your-secret-key-here')

    # Session/Cookie Configuration
    app.config['SESSION_COOKIE_SECURE'] = os.getenv('SESSION_COOKIE_SECURE',
                                                    'False').lower() == 'true'
    app.config['SESSION_COOKIE_HTTPONLY'] = os.getenv('SESSION_COOKIE_HTTPONLY',
                                                      'True').lower() == 'true'
    app.config['SESSION_COOKIE_SAMESITE'] = os.getenv('SESSION_COOKIE_SAMESITE', 'None')
    app.config['REMEMBER_COOKIE_DURATION'] = int(
        os.getenv('REMEMBER_COOKIE_DURATION', '2592000'))  # 30 days in seconds

    # Feature Flags
    app.config['ENABLE_AI_BOT'] = os.getenv('ENABLE_AI_BOT', 'True').lower() == 'true'
    app.config['AI_BOT_CHANNEL_NAME'] = os.getenv('AI_BOT_CHANNEL_NAME', 'ai-helpdesk')

    # Initialize extensions
    db.init_app(app)

    # Configure logging
    app.logger.setLevel(logging.INFO)

    # Register CLI commands
    app.cli.add_command(init_db_command)
    app.cli.add_command(drop_db_command)
    app.cli.add_command(seed_ai_bot_command)

    return app


# --------------------- CLI Commands ---------------------

@click.command('init-db')
@with_appcontext
def init_db_command() -> None:
    """
    Initialize the database tables.

    This command creates all tables defined in the models.
    It's safe to run this command even if tables already exist.
    """
    db.create_all()
    click.echo('Initialized the database.')


@click.command('drop-db')
@with_appcontext
def drop_db_command() -> None:
    """
    Drop all database tables.

    This command removes all tables and data from the database.
    It requires confirmation before proceeding to prevent accidental data loss.
    """
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('Dropped all tables.')


@click.command('seed-ai-bot')
@with_appcontext
def seed_ai_bot_command() -> None:
    """
    Create the AI bot user if it doesn't exist.

    This command checks if the AI bot user exists and creates it if not.
    The AI bot user is used for automated responses in the AI helpdesk channel.
    """
    if not db.session.get(UserModel, "ai_bot"):
        bot_user = UserModel(id="ai_bot", username="ai_bot")
        db.session.add(bot_user)
        db.session.commit()
        click.echo('AI bot user created.')
    else:
        click.echo('AI bot user already exists.')


app = create_app()

# Initialize Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = None  # Disable automatic redirects


@login_manager.user_loader
def load_user(user_id: str) -> Optional[UserModel]:
    """
    Load a user by ID for Flask-Login.

    Args:
        user_id (str): The ID of the user to load.

    Returns:
        Optional[UserModel]: The user object if found, None otherwise.
    """
    return db.session.get(UserModel, user_id)


# Helper function to authenticate a user using either session or token
def get_authenticated_user():
    """
    Helper function to authenticate a user using either session or token.

    Returns:
        Tuple[UserModel, bool]: A tuple containing the authenticated user and a boolean
                               indicating if authentication was successful.
    """
    # Check if user is authenticated via session
    if current_user.is_authenticated:
        app.logger.info(
            f"Session authentication successful for user: {current_user.username}")
        return current_user, True

    # If not, check for token authentication
    auth_header = request.headers.get('Authorization')
    app.logger.info(f"Auth header: {auth_header}")

    if not auth_header or not auth_header.startswith('Bearer '):
        app.logger.warning("No valid Authorization header found")
        return None, False

    token = auth_header.split(' ')[1]
    payload = decode_token(token)

    if not payload:
        app.logger.warning("Invalid token payload")
        return None, False

    user_id = payload.get('sub')
    if not user_id:
        app.logger.warning("No user_id in token payload")
        return None, False

    # Verify user exists
    user = db.session.get(UserModel, user_id)
    if not user:
        app.logger.warning(f"User not found for ID: {user_id}")
        return None, False

    app.logger.info(f"Token authentication successful for user: {user.username}")
    return user, True


@app.route("/")
def home() -> str:
    """
    Serve the home page of the API.

    Returns:
        str: A welcome message for the API.
    """
    return "Welcome to the Chat Client API!"


# --------------------- User Endpoints ---------------------

@app.route("/register", methods=["POST"])
def register() -> Tuple[Response, int]:
    """
    Register a new user with enhanced error logging.
    """
    try:
        data = request.get_json(silent=True)
        if not data:
            app.logger.warning("Registration attempt with invalid or missing JSON")
            return jsonify({"error": "Invalid or missing JSON"}), 400

        username = data.get("username")
        password = data.get("password")

        app.logger.info(f"Registration attempt for username: {username}")

        if not username or not password:
            app.logger.warning("Registration attempt missing username or password")
            return jsonify({"error": "Username and password are required"}), 400

        existing_user = UserModel.query.filter_by(username=username).first()
        if existing_user:
            app.logger.warning(
                f"Registration failed: Username '{username}' already exists")
            return jsonify({"error": "User already exists"}), 400

        # Create new user with proper password hashing
        new_user = UserModel(username=username)
        new_user.set_password(password)

        app.logger.info(f"Created user with ID: {new_user.id}, username: {username}")

        db.session.add(new_user)

        try:
            db.session.commit()
            app.logger.info(f"User saved to database: {username}")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Database error during registration: {str(e)}")
            return jsonify(
                {"error": f"Registration failed: Database error: {str(e)}"}), 500

        # Log the user in after registration
        try:
            login_user(new_user)
            app.logger.info(f"Flask-Login session created for new user: {username}")
        except Exception as e:
            app.logger.error(f"Flask-Login error during registration: {str(e)}")
            # Continue anyway - token-based auth might still work

        # Generate token
        try:
            token = generate_token(new_user.id)
            app.logger.info(f"Generated token for new user {username}: {token[:10]}...")
        except Exception as e:
            app.logger.error(f"Token generation error during registration: {str(e)}")
            return jsonify({
                "error": f"Registration successful, but failed to generate authentication token: {str(e)}"}), 500

        response = {
            "user_id": new_user.id,
            "username": new_user.username,
            "token": token
        }

        app.logger.info(f"Registration successful for user: {username}")
        return jsonify(response), 200

    except Exception as e:
        app.logger.error(f"Unexpected error during registration: {str(e)}")
        return jsonify({"error": f"Registration failed: {str(e)}"}), 500


@app.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Log in an existing user with detailed error logging.
    """
    data = request.get_json(silent=True)
    if not data:
        app.logger.warning("Login attempt with invalid or missing JSON")
        return jsonify({"error": "Invalid or missing JSON"}), 400

    username = data.get("username")
    password = data.get("password")

    app.logger.info(f"Login attempt for username: {username}")

    if not username or not password:
        app.logger.warning("Login attempt missing username or password")
        return jsonify({"error": "Username and password are required"}), 400

    # Find the user
    user = UserModel.query.filter_by(username=username).first()

    if not user:
        app.logger.warning(f"Login failed: User '{username}' not found")
        return jsonify({"error": "Invalid username or password"}), 401

    # Check password
    if not hasattr(user, 'check_password'):
        app.logger.error(f"User model for '{username}' missing check_password method")
        return jsonify({"error": "Authentication system misconfigured"}), 500

    app.logger.info(f"Checking password for user: {username}")

    if not user.check_password(password):
        app.logger.warning(f"Login failed: Invalid password for user '{username}'")
        return jsonify({"error": "Invalid username or password"}), 401

    app.logger.info(f"Password check passed for user: {username}")

    # Log the user in using Flask-Login
    try:
        login_user(user)
        app.logger.info(f"Flask-Login session created for user: {username}")
    except Exception as e:
        app.logger.error(f"Flask-Login error: {str(e)}")
        return jsonify({"error": f"Login session error: {str(e)}"}), 500

    # Generate token
    try:
        token = generate_token(user.id)
        app.logger.info(f"Generated token for user {username}: {token[:10]}...")
    except Exception as e:
        app.logger.error(f"Token generation error: {str(e)}")
        return jsonify(
            {"error": f"Failed to generate authentication token: {str(e)}"}), 500

    response = {
        "user_id": user.id,
        "username": user.username,
        "token": token
    }

    app.logger.info(f"Login successful for user: {username}")
    return jsonify(response), 200


@app.route("/logout", methods=["POST"])
def logout() -> Tuple[Response, int]:
    """
    Log out the current user.
    Supports both session and token authentication.

    Returns:
        Response: A JSON response with logout status.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    # Perform logout for session-based auth
    if current_user.is_authenticated:
        username = current_user.username
        logout_user()
        app.logger.info(f"Session logout successful for user: {username}")

    # For token-based auth, we don't need to do anything server-side
    # The client should discard the token

    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/api/token", methods=["POST"])
def get_token() -> Tuple[Response, int]:
    """
    Generate an API token for a user.

    This endpoint allows clients to get a token without using session cookies.
    Expects JSON with username and password fields.
    Returns only the token for API usage.

    Returns:
        Tuple[Response, int]: A JSON response with the token and HTTP status code
    """
    data: Dict[str, Any] = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    username: str = data.get("username")
    password: str = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    # Find and validate the user
    user = UserModel.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Generate a token
    token = generate_token(user.id)

    return jsonify({"token": token}), 200


@app.route("/api/me", methods=["GET"])
@token_required
def get_user_profile(current_user):
    """
    Get the current user's profile using token authentication.

    This endpoint demonstrates using token authentication without sessions.
    The @token_required decorator injects the current_user based on the token.

    Args:
        current_user: The authenticated user (injected by the decorator)

    Returns:
        Response: A JSON response with the user's profile information
    """
    return jsonify({
        "id": current_user.id,
        "username": current_user.username
    })


# --------------------- Channel Endpoints ---------------------

@app.route("/channel", methods=["POST"])
def create_channel() -> Tuple[Response, int]:
    """
    Create a new chat channel.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name = data.get("name")
    if not name:
        return jsonify({"error": "Channel name is required"}), 400

    new_channel = ChannelModel(id=str(uuid.uuid4()), name=name)
    db.session.add(new_channel)

    try:
        db.session.commit()
        app.logger.info(f"Channel '{name}' created by user: {user.username}")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error creating channel: {str(e)}")
        return jsonify({"error": f"Failed to create channel: {str(e)}"}), 500

    return jsonify({"channel_id": new_channel.id, "name": new_channel.name}), 200


@app.route("/channel/join", methods=["POST"])
def join_channel() -> Tuple[Response, int]:
    """
    Join a user to a channel.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use the authenticated user's ID
    user_id = user.id
    channel_id = data.get("channel_id")

    if not channel_id:
        return jsonify({"error": "Channel ID is required"}), 400

    # Validate channel exists
    channel = db.session.get(ChannelModel, channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    # Check if user is already a member
    existing_membership = ChannelUserModel.query.filter_by(
        user_id=user_id,
        channel_id=channel_id
    ).first()

    if existing_membership:
        return jsonify(
            {"joined": True, "message": "User already joined this channel"}), 200

    # Create new membership
    membership = ChannelUserModel(user_id=user_id, channel_id=channel_id)
    db.session.add(membership)

    try:
        db.session.commit()
        app.logger.info(f"User {user.username} joined channel: {channel.name}")
        return jsonify({"joined": True}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error joining channel: {str(e)}")
        return jsonify({"error": "Failed to join channel due to a server error"}), 500


@app.route("/channel/<channel_id>/users", methods=["GET"])
def list_channel_users(channel_id: str) -> Tuple[Response, int]:
    """
    List all users who have joined a channel.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    # Check if channel exists
    channel = db.session.get(ChannelModel, channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    # Get all user IDs from the channel_users table
    memberships = ChannelUserModel.query.filter_by(channel_id=channel_id).all()
    user_ids = [membership.user_id for membership in memberships]

    # Fetch user details for each user ID
    user_details = []
    for user_id in user_ids:
        user = db.session.get(UserModel, user_id)
        if user:
            user_details.append({
                "id": user.id,
                "username": user.username
            })

    app.logger.info(f"Retrieved {len(user_details)} users for channel: {channel.name}")
    return jsonify({"users": user_details})


@app.route("/channels", methods=["GET"])
def list_channels():
    """
    List all available channels.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        app.logger.warning("Authentication failed for /channels request")
        return jsonify({"error": "Authentication required"}), 401

    app.logger.info(f"Listing channels for user: {user.username}")
    channels = ChannelModel.query.all()

    result = [{
        "channel_id": channel.id,
        "name": channel.name
    } for channel in channels]

    app.logger.info(f"Returned {len(result)} channels")
    return jsonify(result)


# --------------------- Message Endpoints ---------------------

@app.route("/message", methods=["POST"])
def send_message() -> Tuple[Response, int]:
    """
    Send a message to a channel.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use the authenticated user's ID
    sender_id = user.id
    channel_id = data.get("channel_id")
    content = data.get("content")

    if not channel_id or not content:
        return jsonify({"error": "Channel ID and content are required"}), 400

    new_message = MessageModel(
        id=str(uuid.uuid4()),
        sender_id=sender_id,
        channel_id=channel_id,
        content=content,
    )
    db.session.add(new_message)

    try:
        db.session.commit()
        app.logger.info(f"Message sent by {user.username} to channel: {channel_id}")
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error sending message: {str(e)}")
        return jsonify({"error": f"Failed to send message: {str(e)}"}), 500

    response_payload = [{
        "message_id": new_message.id,
        "sender_id": new_message.sender_id,
        "channel_id": new_message.channel_id,
        "content": new_message.content,
    }]

    channel = db.session.get(ChannelModel, channel_id)

    if (channel and
            channel.name == app.config['AI_BOT_CHANNEL_NAME'] and
            app.config['ENABLE_AI_BOT']):
        try:
            app.logger.info(f"Processing AI bot response for channel: {channel.name}")
            ai_bot = AiBotChannel()
            ai_response = ai_bot.handle_message(content)

            bot_message = MessageModel(
                id=str(uuid.uuid4()),
                sender_id="ai_bot",
                channel_id=channel_id,
                content=ai_response,
            )
            db.session.add(bot_message)
            db.session.commit()

            response_payload.append({
                "message_id": bot_message.id,
                "sender_id": bot_message.sender_id,
                "channel_id": bot_message.channel_id,
                "content": bot_message.content,
            })

            app.logger.info("AI bot response processed successfully")
        except ImportError as e:
            app.logger.error(f"AI bot module could not be imported: {str(e)}")
        except Exception as e:
            app.logger.error(f"Error processing AI bot response: {str(e)}")

    return jsonify(response_payload)


@app.route("/message/<channel_id>", methods=["GET"])
def fetch_messages(channel_id: str) -> Tuple[Response, int]:
    """
    Fetch all messages from a specific channel.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    # Check if channel exists
    channel = db.session.get(ChannelModel, channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    messages = MessageModel.query.filter_by(channel_id=channel_id).all()

    result = [{
        "message_id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
    } for m in messages]

    app.logger.info(f"Retrieved {len(result)} messages for channel: {channel.name}")
    return jsonify(result)


# --------------------- Direct Messages ---------------------

@app.route("/start_dm", methods=["POST"])
def start_direct_message() -> Tuple[Response, int]:
    """
    Start or retrieve a direct message channel between two users.
    Supports both session and token authentication.
    """
    # Authenticate the user
    user, authenticated = get_authenticated_user()
    if not authenticated:
        return jsonify({"error": "Authentication required"}), 401

    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use the authenticated user's ID
    sender_id = user.id
    receiver_id = data.get("receiver_id")

    if not receiver_id:
        return jsonify({"error": "Receiver ID is required"}), 400

    # Sort user IDs to ensure consistent channel naming
    user_ids = sorted([sender_id, receiver_id])
    channel_name = f"dm_{user_ids[0]}_{user_ids[1]}"

    existing_channel = ChannelModel.query.filter_by(name=channel_name).first()

    if not existing_channel:
        channel = ChannelModel(id=str(uuid.uuid4()), name=channel_name)
        db.session.add(channel)

        try:
            db.session.commit()
            app.logger.info(f"Created DM channel between {sender_id} and {receiver_id}")
        except Exception as e:
            db.session.rollback()
            app.logger.error(f"Error creating DM channel: {str(e)}")
            return jsonify({"error": f"Failed to create DM channel: {str(e)}"}), 500
    else:
        channel = existing_channel
        app.logger.info(
            f"Using existing DM channel between {sender_id} and {receiver_id}")

    return jsonify({"channel_id": channel.id})


# ------------------ Flask Error Handlers ------------------
@login_manager.unauthorized_handler
def unauthorized() -> Tuple[Response, int]:
    """Custom handler for unauthorized requests"""
    return jsonify({"error": "Authentication required"}), 401


@app.errorhandler(400)
def bad_request(error) -> Tuple[Response, int]:
    """Handles HTTP 400 Bad Request errors."""
    app.logger.warning(f"400 Bad Request: {str(error)}")
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@app.errorhandler(404)
def not_found(error) -> Tuple[Response, int]:
    """Handles HTTP 404 Not Found errors."""
    app.logger.warning(f"404 Not Found: {str(error)}")
    return jsonify({"error": "Not found", "message": str(error)}), 404


@app.errorhandler(500)
def internal_server_error(error) -> Tuple[Response, int]:
    """Handles HTTP 500 Internal Server errors."""
    app.logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(Exception)
def unhandled_exception(error) -> Tuple[Response, int]:
    """Catches and handles uncaught exceptions."""
    app.logger.exception(f"Unhandled Exception: {str(error)}")
    return jsonify({"error": "An unexpected error occurred"}), 500


@app.route("/test-auth", methods=["GET"])
def test_auth() -> Tuple[Response, int]:
    """
    Simple endpoint to test if authentication is working.
    Returns different responses for authenticated and unauthenticated requests.
    """
    user, authenticated = get_authenticated_user()

    if authenticated:
        return jsonify({
            "authenticated": True,
            "user_id": user.id,
            "username": user.username,
            "auth_type": "session" if current_user.is_authenticated else "token",
            "time": str(datetime.datetime.now())
        }), 200
    else:
        return jsonify({
            "authenticated": False,
            "message": "Authentication required to access protected resources",
            "time": str(datetime.datetime.now())
        }), 401


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])