from flask import Flask, jsonify, request
from src.models import db
from src.models.channel_model import ChannelModel
from src.models.message_model import MessageModel
from src.models.user_model import UserModel
import uuid
import logging
import os
import click
from flask.cli import with_appcontext
from flask_cors import CORS
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()


def create_app():
    """
    Create and configure the Flask application.

    Returns:
        Flask: The configured Flask application.
    """
    app = Flask(__name__)
    CORS(app)

    # Database Configuration from environment variables
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    DB_PATH = os.getenv('DB_PATH', 'chat.db')
    app.config["SQLALCHEMY_DATABASE_URI"] = f"{DB_TYPE}:///{DB_PATH}"
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
def init_db_command():
    """Initialize the database tables."""
    db.create_all()
    click.echo('Initialized the database.')


@click.command('drop-db')
@with_appcontext
def drop_db_command():
    """Drop all database tables."""
    if click.confirm('Are you sure you want to drop all tables?'):
        db.drop_all()
        click.echo('Dropped all tables.')


@click.command('seed-ai-bot')
@with_appcontext
def seed_ai_bot_command():
    """Create the AI bot user if it doesn't exist."""
    if not db.session.get(UserModel, "ai_bot"):
        bot_user = UserModel(id="ai_bot", username="ai_bot")
        db.session.add(bot_user)
        db.session.commit()
        click.echo('AI bot user created.')
    else:
        click.echo('AI bot user already exists.')


app = create_app()


@app.route("/")
def home():
    return "Welcome to the Chat Client API!"


# --------------------- User Endpoints ---------------------

@app.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")

    existing_user = UserModel.query.filter_by(username=username).first()
    if existing_user:
        return jsonify({"error": "User already exists"}), 400

    new_user = UserModel(id=str(uuid.uuid4()), username=username)
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"user_id": new_user.id, "username": new_user.username})


@app.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get("username")

    user = UserModel.query.filter_by(username=username).first()
    if not user:
        return jsonify({"error": "User does not exist"}), 404

    return jsonify({"user_id": user.id, "username": user.username})


# --------------------- Channel Endpoints ---------------------

@app.route("/channel", methods=["POST"])
def create_channel():
    data = request.get_json()
    name = data.get("name")

    new_channel = ChannelModel(id=str(uuid.uuid4()), name=name)
    db.session.add(new_channel)
    db.session.commit()

    return jsonify({"channel_id": new_channel.id, "name": new_channel.name})


@app.route("/channel/join", methods=["POST"])
def join_channel():
    data = request.get_json()
    user_id = data.get("user_id")
    channel_id = data.get("channel_id")

    user = db.session.get(UserModel, user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    channel = db.session.get(ChannelModel, channel_id)
    if not channel:
        return jsonify({"error": "Channel not found"}), 404

    # TODO: Implement join table
    return jsonify({"joined": True})


@app.route("/channel/<channel_id>/users", methods=["GET"])
def list_channel_users(channel_id):
    messages = MessageModel.query.filter_by(channel_id=channel_id).all()
    user_ids = list({msg.sender_id for msg in messages})
    return jsonify({"users": user_ids})


@app.route("/channels", methods=["GET"])
def list_channels():
    channels = ChannelModel.query.all()
    return jsonify([{
        "channel_id": channel.id,
        "name": channel.name
    } for channel in channels])


# --------------------- Message Endpoints ---------------------

@app.route("/message", methods=["POST"])
def send_message():
    data = request.get_json()
    sender_id = data.get("sender_id")
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
            from src.channel_impl.ai_bot_channel import AiBotChannel
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
        except ImportError as e:
            app.logger.error(f"AI bot module could not be imported: {str(e)}")
        except Exception as e:
            app.logger.error(f"Error processing AI bot response: {str(e)}")

    return jsonify(response_payload)


@app.route("/message/<channel_id>", methods=["GET"])
def fetch_messages(channel_id):
    messages = MessageModel.query.filter_by(channel_id=channel_id).all()
    return jsonify([{
        "message_id": m.id,
        "sender_id": m.sender_id,
        "content": m.content,
    } for m in messages])


# --------------------- Direct Messages ---------------------

@app.route("/start_dm", methods=["POST"])
def start_direct_message():
    data = request.get_json()
    sender_id = data["sender_id"]
    receiver_id = data["receiver_id"]

    # Sort user IDs to ensure consistent channel naming
    user_ids = sorted([sender_id, receiver_id])
    channel_name = f"dm_{user_ids[0]}_{user_ids[1]}"

    existing_channel = ChannelModel.query.filter_by(name=channel_name).first()

    if not existing_channel:
        channel = ChannelModel(id=str(uuid.uuid4()), name=channel_name)
        db.session.add(channel)
        db.session.commit()
    else:
        channel = existing_channel

    return jsonify({"channel_id": channel.id})


if __name__ == "__main__":
    app.run(debug=app.config['DEBUG'])