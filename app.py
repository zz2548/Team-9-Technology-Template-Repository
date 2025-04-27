import logging
import uuid

from flask import Flask, jsonify, request
from flask_cors import CORS

from src.models import db
from src.models.channel_model import ChannelModel
from src.models.message_model import MessageModel
from src.models.user_model import UserModel

app = Flask(__name__)
CORS(app)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///chat.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)
app.logger.setLevel(logging.INFO)

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

    user = UserModel.query.get(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    channel = ChannelModel.query.get(channel_id)
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
        "name": channel.name,
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

    channel = ChannelModel.query.get(channel_id)

    if channel and channel.name == "ai-helpdesk":
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

    channel_name = f"dm_{sender_id}_{receiver_id}"
    existing_channel = ChannelModel.query.filter_by(name=channel_name).first()

    if not existing_channel:
        channel = ChannelModel(id=str(uuid.uuid4()), name=channel_name)
        db.session.add(channel)
        db.session.commit()
    else:
        channel = existing_channel

    return jsonify({"channel_id": channel.id})

# --------------------- AI Bot Setup ---------------------

def ensure_ai_bot_user():
    from src.models.user_model import UserModel
    if not UserModel.query.get("ai_bot"):
        bot_user = UserModel(id="ai_bot", username="ai_bot")
        db.session.add(bot_user)
        db.session.commit()

if __name__ == "__main__":
    with app.app_context():
        ensure_ai_bot_user()
    app.run()
