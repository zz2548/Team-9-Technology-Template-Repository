from flask import Flask, jsonify, request, Response
from src.models import db
from src.models.channel_model import ChannelModel
from src.models.message_model import MessageModel
from src.models.user_model import UserModel
from src.models.channel_user_model import ChannelUserModel
from src.auth import generate_token, token_required
from src.channel_impl.ai_bot_channel import AiBotChannel
import uuid
import logging
import os
import click
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
    CORS(app)

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
login_manager.login_view = "login"  # Specify the login view route name


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
    Register a new user in the system.

    Expects a JSON payload with 'username' and 'password' fields.
    Checks if the username is already taken before creating a new user.
    Logs the user in after successful registration.

    Returns:
        tuple: A JSON response with user details and HTTP status code.
               Success: ({"user_id": id, "username": username, "token": token}, 200)
               Error: ({"error": message}, error_code)
    """
    data: Dict[str, Any] = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    username: str = data.get("username")
    password: str = data.get("password")  # You now need to require a password

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    existing_user: Optional[UserModel] = UserModel.query.filter_by(
        username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = UserModel(username=username, password=password)
    db.session.add(new_user)
    db.session.commit()

    # Log the user in after registration
    login_user(new_user)

    token = generate_token(new_user.id)
    response = {
        "user_id": new_user.id,
        "username": new_user.username,
        "token": token
    }
    return jsonify(response), 200


@app.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Log in an existing user.

    Expects a JSON payload with 'username' and 'password' fields.
    Verifies the user exists in the system and the password is correct.
    Uses Flask-Login to manage the user's session.

    Returns:
        tuple: A JSON response with user details and HTTP status code.
               Success: ({"user_id": id, "username": username, "token": token}, 200)
               Error: ({"error": message}, error_code)
    """
    data: Dict[str, Any] = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    username: str = data.get("username")
    password: str = data.get("password")

    if not username or not password:
        return jsonify({"error": "Username and password are required"}), 400

    user: Optional[UserModel] = UserModel.query.filter_by(username=username).first()
    if not user or not user.check_password(password):
        return jsonify({"error": "Invalid username or password"}), 401

    # Log the user in using Flask-Login
    login_user(user)

    token = generate_token(user.id)
    response = {
        "user_id": user.id,
        "username": user.username,
        "token": token
    }
    return jsonify(response), 200


@app.route("/logout", methods=["POST"])
@login_required
def logout() -> Tuple[Response, int]:
    """
    Log out the current user.

    Requires the user to be authenticated via Flask-Login.
    Ends the user's session.

    Returns:
        tuple: A JSON response with logout status and HTTP status code.
               Success: ({"message": "Logged out successfully"}, 200)
    """
    logout_user()
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
@login_required
def create_channel() -> Tuple[Response, int]:
    """
    Create a new chat channel.

    Expects a JSON payload with a 'name' field for the channel name.

    Returns:
        tuple: A JSON response with channel details and HTTP status code.
               Success: ({"channel_id": id, "name": name}, 200)
    """
    data: Dict[str, Any] = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    name: str = data.get("name")

    new_channel = ChannelModel(id=str(uuid.uuid4()), name=name)
    db.session.add(new_channel)
    db.session.commit()

    return jsonify({"channel_id": new_channel.id, "name": new_channel.name}), 200


@app.route("/channel/join", methods=["POST"])
@login_required
def join_channel() -> Tuple[Response, int]:
    """
    Join a user to a channel.

    Expects a JSON payload with 'user_id' and 'channel_id' fields.
    Validates that both the user and channel exist before joining.
    Creates a record in the channel_users table to represent the membership.

    Returns:
        tuple: A JSON response with join status and HTTP status code.
               Success: ({"joined": True}, 200)
               Error: ({"error": message}, error_code)
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use current_user.id instead of data.get("user_id")
    user_id = current_user.id
    channel_id = data.get("channel_id")

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
        return jsonify({"joined": True}), 200
    except Exception as e:
        db.session.rollback()
        app.logger.error(f"Error joining channel: {str(e)}")
        return jsonify({"error": "Failed to join channel due to a server error"}), 500


@app.route("/channel/<channel_id>/users", methods=["GET"])
@login_required
def list_channel_users(channel_id: str) -> Response:
    """
    List all users who have joined a channel.

    This implementation returns all users who have explicitly joined the channel
    through the join_channel endpoint, addressing the incomplete feature noted
    in the PR feedback.

    Args:
        channel_id (str): The ID of the channel to list users for.

    Returns:
        Response: A JSON response with a list of user IDs.
                 Format: {"users": [user_id1, user_id2, ...]}
    """
    # Check if channel exists
    channel: Optional[ChannelModel] = db.session.get(ChannelModel, channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    # Get all user IDs from the channel_users table
    memberships = ChannelUserModel.query.filter_by(channel_id=channel_id).all()
    user_ids: List[str] = [membership.user_id for membership in memberships]

    # Fetch user details for each user ID
    user_details = []
    for user_id in user_ids:
        user = db.session.get(UserModel, user_id)
        if user:
            user_details.append({
                "id": user.id,
                "username": user.username
            })
    return jsonify({"users": user_details})


@app.route("/channels", methods=["GET"])
@login_required
def list_channels() -> Response:
    """
    List all available channels.

    Returns:
        Response: A JSON response with a list of channel details.
                 Format: [{"channel_id": id1, "name": name1}, ...]
    """
    channels: List[ChannelModel] = ChannelModel.query.all()
    return jsonify([{
        "channel_id": channel.id,
        "name": channel.name
    } for channel in channels])


# --------------------- Message Endpoints ---------------------

@app.route("/message", methods=["POST"])
@login_required
def send_message() -> Response:
    """
    Send a message to a channel.

    Expects a JSON payload with 'sender_id', 'channel_id', and 'content' fields.
    If the channel is the AI helpdesk channel and AI bot is enabled,
    it will also generate and return an AI response.

    Returns:
        Response: A JSON response with message details, and AI response if applicable.
                 Format: [{"message_id": id, "sender_id": sender, ...}, ...]
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use current_user.id instead of data.get("sender_id")
    sender_id = current_user.id
    channel_id = data.get("channel_id")
    content = data.get("content")

    new_message = MessageModel(
        id=str(uuid.uuid4()),
        sender_id=sender_id,
        channel_id=channel_id,
        content=content,
    )
    db.session.add(new_message)
    db.session.commit()

    response_payload: List[Dict[str, str]] = [{
        "message_id": new_message.id,
        "sender_id": new_message.sender_id,
        "channel_id": new_message.channel_id,
        "content": new_message.content,
    }]

    channel: Optional[ChannelModel] = db.session.get(ChannelModel, channel_id)

    if (channel and
            channel.name == app.config['AI_BOT_CHANNEL_NAME'] and
            app.config['ENABLE_AI_BOT']):
        try:

            ai_bot = AiBotChannel()
            ai_response: str = ai_bot.handle_message(content)

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
        except ImportError as e:
            app.logger.error(f"AI bot module could not be imported: {str(e)}")
        except Exception as e:
            app.logger.error(f"Error processing AI bot response: {str(e)}")

    return jsonify(response_payload)


@app.route("/message/<channel_id>", methods=["GET"])
@login_required
def fetch_messages(channel_id: str) -> Response:
    """
    Fetch all messages from a specific channel.

    Args:
        channel_id (str): The ID of the channel to fetch messages from.

    Returns:
        Response: A JSON response with a list of message details.
                 Format: [{"message_id": id, "sender_id": sender, "content": text}, ...]
    """
    messages: List[MessageModel] = MessageModel.query.filter_by(
        channel_id=channel_id).all()
    return jsonify([{
        "message_id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
    } for m in messages])


# --------------------- Direct Messages ---------------------

@app.route("/start_dm", methods=["POST"])
@login_required
def start_direct_message() -> Response:
    """
    Start or retrieve a direct message channel between two users.

    Expects a JSON payload with 'sender_id' and 'receiver_id' fields.
    Creates a new DM channel if one doesn't exist, or returns the existing one.

    The channel name is created by sorting the user IDs to ensure uniqueness
    regardless of which user initiates the conversation.

    Returns:
        Response: A JSON response with the channel ID.
                 Format: {"channel_id": id}
    """
    data = request.get_json(silent=True)
    if not data:
        return jsonify({"error": "Invalid or missing JSON"}), 400

    # Use current_user.id instead of data.get("sender_id")
    sender_id = current_user.id
    receiver_id = data.get("receiver_id")

    # Sort user IDs to ensure consistent channel naming
    user_ids: List[str] = sorted([sender_id, receiver_id])
    channel_name: str = f"dm_{user_ids[0]}_{user_ids[1]}"

    existing_channel: Optional[ChannelModel] = ChannelModel.query.filter_by(
        name=channel_name).first()

    if not existing_channel:
        channel = ChannelModel(id=str(uuid.uuid4()), name=channel_name)
        db.session.add(channel)
        db.session.commit()
    else:
        channel = existing_channel

    return jsonify({"channel_id": channel.id})


# ------------------ Flask Error Handlers ------------------

@app.errorhandler(400)
def bad_request(error):
    """Handles HTTP 400 Bad Request errors."""
    app.logger.warning(f"400 Bad Request: {str(error)}")
    return jsonify({"error": "Bad request", "message": str(error)}), 400


@app.errorhandler(404)
def not_found(error):
    """Handles HTTP 404 Not Found errors."""
    app.logger.warning(f"404 Not Found: {str(error)}")
    return jsonify({"error": "Not found", "message": str(error)}), 404


@app.errorhandler(500)
def internal_server_error(error):
    """Handles HTTP 500 Internal Server errors."""
    app.logger.error(f"500 Internal Server Error: {str(error)}")
    return jsonify({"error": "Internal server error"}), 500


@app.errorhandler(Exception)
def unhandled_exception(error):
    """Catches and handles uncaught exceptions."""
    app.logger.exception(f"Unhandled Exception: {str(error)}")
    return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])