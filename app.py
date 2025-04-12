from flask import Flask, request, jsonify
from src.user import User
from src.channel import Channel
from src.message import Message

app = Flask(__name__)

# In-memory user store
users = {}  # username -> User instance
messages_by_channel = {}  # channel_id -> list of Message instances

@app.route('/')
def home():
    return 'Welcome to the Chat Client API!'

# User Endpoints
@app.route('/register', methods=['POST'])
def register():
    data = request.get_json()
    username = data.get('username')

    if username in users:
        return jsonify({"error": "User already exists"}), 400

    user = User.register(username)
    users[username] = user
    return jsonify({"user_id": user.get_id(), "username": user.get_username()})


@app.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')

    if username not in users:
        return jsonify({"error": "User does not exist"}), 404

    user = users[username]
    return jsonify({"user_id": user.get_id(), "username": user.get_username()})


# Channel Endpoints
@app.route('/channel', methods=['POST'])
def create_channel():
    data = request.get_json()
    name = data.get('name')

    channel = Channel.create_channel(name)
    return jsonify({"channel_id": channel.get_id(), "name": channel.get_name()})


@app.route('/channel/join', methods=['POST'])
def join_channel():
    data = request.get_json()
    user_id = data.get('user_id')
    channel_id = data.get('channel_id')

    success = Channel.join_channel(user_id, channel_id)
    return jsonify({"joined": success})


@app.route('/channel/<channel_id>/users', methods=['GET'])
def list_channel_users(channel_id):
    channel = Channel(channel_id, "dummy")  # only needs ID for accessing list
    users_in_channel = channel.list_users()
    return jsonify({"users": users_in_channel})


# Message Endpoints
@app.route('/message', methods=['POST'])
def send_message():
    data = request.get_json()
    sender_id = data.get('sender_id')
    channel_id = data.get('channel_id')
    content = data.get('content')

    msg = Message.send_message(sender_id, channel_id, content)
    messages_by_channel.setdefault(channel_id, []).append(msg)

    return jsonify({
        "message_id": msg.get_id(),
        "sender_id": msg.get_sender(),
        "channel_id": msg.get_channel(),
        "content": msg.get_content()
    })


@app.route('/message/<channel_id>', methods=['GET'])
def fetch_messages(channel_id):
    messages = messages_by_channel.get(channel_id, [])
    return jsonify([{
        "message_id": m.get_id(),
        "sender_id": m.get_sender(),
        "content": m.get_content()
    } for m in messages])


if __name__ == "__main__":
    app.run(debug=True)
