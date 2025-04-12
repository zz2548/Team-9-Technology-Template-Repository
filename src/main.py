from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory storage for simplicity
messages = []


@app.route("/messages", methods=["GET"])
def get_messages():
    return jsonify(messages)


@app.route("/messages", methods=["POST"])
def post_message():
    data = request.json
    username = data.get("username")
    content = data.get("content")
    if username and content:
        messages.append({"user": username, "content": content})
        return jsonify({"status": "Message sent!"}), 201
    return jsonify({"error": "Invalid data"}), 400


if __name__ == "__main__":
    app.run(debug=True)
