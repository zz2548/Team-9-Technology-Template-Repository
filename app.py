from flask import Flask, jsonify, request, Response
from src.models import db
from src.models.channel_model import ChannelModel
from src.models.message_model import MessageModel
from src.models.user_model import UserModel
from src.models.channel_user_model import ChannelUserModel
import uuid
import logging
import os
import click
from flask.cli import with_appcontext
from flask_cors import CORS
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

    Expects a JSON payload with a 'username' field.
    Checks if the username is already taken before creating a new user.

    Returns:
        tuple: A JSON response with user details and HTTP status code.
               Success: ({"user_id": id, "username": username}, 200)
               Error: ({"error": message}, error_code)
    """
    data: Dict[str, Any] = request.get_json()
    username: str = data.get("username")

    existing_user: Optional[UserModel] = UserModel.query.filter_by(
        username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = UserModel(id=str(uuid.uuid4()), username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user_id": new_user.id, "username": new_user.username}), 200


@app.route("/login", methods=["POST"])
def login() -> Tuple[Response, int]:
    """
    Log in an existing user.

    Expects a JSON payload with a 'username' field.
    Verifies the user exists in the system.

    Returns:
        tuple: A JSON response with user details and HTTP status code.
               Success: ({"user_id": id, "username": username}, 200)
               Error: ({"error": message}, error_code)
    """
    data: Dict[str, Any] = request.get_json()
    username: str = data.get("username")

    user: Optional[UserModel] = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify({"user_id": user.id, "username": user.username}), 200


# --------------------- Channel Endpoints ---------------------

@app.route("/channel", methods=["POST"])
def create_channel() -> Tuple[Response, int]:
    """
    Create a new chat channel.

    Expects a JSON payload with a 'name' field for the channel name.

    Returns:
        tuple: A JSON response with channel details and HTTP status code.
               Success: ({"channel_id": id, "name": name}, 200)
    """
    data: Dict[str, Any] = request.get_json()
    name: str = data.get("name")

    new_channel = ChannelModel(id=str(uuid.uuid4()), name=name)
    db.session.add(new_channel)
    db.session.commit()

    return jsonify({"channel_id": new_channel.id, "name": new_channel.name}), 200


"""
Replace the existing join_channel function with this implementation.
"""


@app.route("/channel/join", methods=["POST"])
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
    data: Dict[str, Any] = request.get_json()
    user_id: str = data.get("user_id")
    channel_id: str = data.get("channel_id")

    # Validate user exists
    user: Optional[UserModel] = db.session.get(UserModel, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Validate channel exists
    channel: Optional[ChannelModel] = db.session.get(ChannelModel, channel_id)
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

    return jsonify({"users": user_ids})


@app.route("/channels", methods=["GET"])
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
    data: Dict[str, Any] = request.get_json()
    sender_id: str = data.get("sender_id")
    channel_id: str = data.get("channel_id")
    content: str = data.get("content")

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
            # Lazy import of AiBotChannel to handle potential missing dependency
            from src.channel_impl.ai_bot_channel import AiBotChannel
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
    data: Dict[str, Any] = request.get_json()
    sender_id: str = data["sender_id"]
    receiver_id: str = data["receiver_id"]

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


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])