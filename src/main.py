from flask import Flask, request, jsonify, session
from flask_cors import CORS
import uuid
from datetime import datetime
from user import User

app = Flask(__name__)
app.secret_key = "your-secret-key-here"  # Change this in production
CORS(app, supports_credentials=True)  # Enable CORS with credentials

# In-memory storage for channels and messages
channels = {
    "general": {"name": "general", "users": []},
    "random": {"name": "random", "users": []}
}
messages = []


# Routes for user management
@app.route("/api/register", methods=["POST"])
def register():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.register(username)
    if not user:
        return jsonify({"error": "Username already taken"}), 409

    # Add user to default channels
    for channel_name in user.list_channels():
        if channel_name in channels:
            channels[channel_name]["users"].append(user.get_id())

    session["user_id"] = user.get_id()
    return jsonify(user.to_dict()), 201


@app.route("/api/login", methods=["POST"])
def login():
    data = request.json
    username = data.get("username")

    if not username:
        return jsonify({"error": "Username is required"}), 400

    user = User.login(username)
    if not user:
        return jsonify({"error": "User not found"}), 404

    session["user_id"] = user.get_id()
    return jsonify(user.to_dict()), 200


@app.route("/api/logout", methods=["POST"])
def logout():
    session.pop("user_id", None)
    return jsonify({"message": "Logged out successfully"}), 200


@app.route("/api/current_user", methods=["GET"])
def current_user():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    user = User.get_by_id(user_id)
    if not user:
        session.pop("user_id", None)
        return jsonify({"error": "User not found"}), 404

    return jsonify(user.to_dict()), 200


# Routes for channels
@app.route("/api/channels", methods=["GET"])
def list_channels():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    channel_list = [
        {"id": c_name, "name": c_info["name"]}
        for c_name, c_info in channels.items()
    ]
    return jsonify(channel_list), 200


@app.route("/api/channels", methods=["POST"])
def create_channel():
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    data = request.json
    name = data.get("name")

    if not name:
        return jsonify({"error": "Channel name is required"}), 400

    if name in channels:
        return jsonify({"error": "Channel already exists"}), 409

    # Create new channel
    channels[name] = {"name": name, "users": [user_id]}

    # Add channel to user's list
    user = User.get_by_id(user_id)
    if user:
        user.join_channel(name)

    return jsonify({"id": name, "name": name}), 201


@app.route("/api/channels/<channel_id>/join", methods=["POST"])
def join_channel(channel_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    if channel_id not in channels:
        return jsonify({"error": "Channel not found"}), 404

    user = User.get_by_id(user_id)
    if not user:
        return jsonify({"error": "User not found"}), 404

    # Add channel to user's list
    user.join_channel(channel_id)

    # Add user to channel's list
    if user_id not in channels[channel_id]["users"]:
        channels[channel_id]["users"].append(user_id)

    return jsonify({"message": "Joined channel successfully"}), 200


@app.route("/api/channels/<channel_id>/users", methods=["GET"])
def list_channel_users(channel_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    if channel_id not in channels:
        return jsonify({"error": "Channel not found"}), 404

    channel_users = []
    for u_id in channels[channel_id]["users"]:
        user = User.get_by_id(u_id)
        if user:
            channel_users.append({
                "id": user.get_id(),
                "username": user.get_username()
            })

    return jsonify(channel_users), 200


# Routes for messages
@app.route("/api/channels/<channel_id>/messages", methods=["GET"])
def get_messages(channel_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    if channel_id not in channels:
        return jsonify({"error": "Channel not found"}), 404

    user = User.get_by_id(user_id)
    if not user or channel_id not in user.list_channels():
        return jsonify({"error": "Not a member of this channel"}), 403

    # Filter messages by channel
    channel_messages = [msg for msg in messages if msg.get("channel_id") == channel_id]

    # Sort by timestamp (newest first)
    channel_messages.sort(key=lambda x: x.get("timestamp", ""), reverse=True)

    # Limit to the last 50 messages
    limit = int(request.args.get("limit", 50))
    channel_messages = channel_messages[:limit]

    return jsonify(channel_messages), 200


@app.route("/api/channels/<channel_id>/messages", methods=["POST"])
def send_message(channel_id):
    user_id = session.get("user_id")
    if not user_id:
        return jsonify({"error": "Not logged in"}), 401

    if channel_id not in channels:
        return jsonify({"error": "Channel not found"}), 404

    user = User.get_by_id(user_id)
    if not user or channel_id not in user.list_channels():
        return jsonify({"error": "Not a member of this channel"}), 403

    data = request.json
    content = data.get("content")

    if not content:
        return jsonify({"error": "Message content is required"}), 400

    # Create new message
    message = {
        "id": str(uuid.uuid4()),
        "user_id": user_id,
        "username": user.get_username(),
        "channel_id": channel_id,
        "content": content,
        "timestamp": datetime.now().isoformat()
    }

    messages.append(message)
    return jsonify(message), 201


if __name__ == "__main__":
    app.run(debug=True)