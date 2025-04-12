# Chat Client API 

This project implements a basic **chat client server** in Python using **Flask** and **SQLite**.  
It provides RESTful APIs for:

- User registration and login
- Creating and joining chat channels
- Sending and fetching messages
- Direct messaging between two users

It also includes CI/CD integration with **CircleCI** and dependency management with **uv**.

---

# Features

- **Register** new users
- **Login** existing users
- **Create Channels**
- **Join Channels**
- **Send Messages** to channels
- **Fetch Messages** from channels
- **Start Direct Messages** between two users
- **Persistent database** using SQLite
- **Unit and Integration tests** using pytest, nose2
- **Static analysis** using mypy and ruff
- **CircleCI** pipeline for automated testing and linting

---

# Running the Server

First, initialize the database:

```bash
$env:FLASK_APP = "app.py"     # (Windows PowerShell)
flask shell
>>> from src.models import db
>>> db.create_all()
>>> exit()
```

Then start the Flask server:

```bash
python app.py
```

👉️ Server will run at: `http://127.0.0.1:5000/`

---

# API Endpoints 

## User Endpoints

### POST `/register`
- Register a new user.
- **Body:**
```json
{
  "username": "john_doe"
}
```
- **Success Response:**
```json
{
  "user_id": "john_doe",
  "username": "john_doe"
}
```

### POST `/login`
- Log in an existing user.
- **Body:**
```json
{
  "username": "john_doe"
}
```
- **Success Response:**
```json
{
  "user_id": "john_doe",
  "username": "john_doe"
}
```

## Channel Endpoints

### POST `/channel`
- Create a new chat channel.
- **Body:**
```json
{
  "name": "general"
}
```
- **Success Response:**
```json
{
  "channel_id": "general",
  "name": "general"
}
```

### POST `/channel/join`
- Join an existing channel.
- **Body:**
```json
{
  "user_id": "john_doe",
  "channel_id": "general"
}
```
- **Success Response:**
```json
{
  "joined": true
}
```

### GET `/channel/<channel_id>/users`
- List users in a channel.
- **Response:**
```json
{
  "users": ["john_doe"]
}
```

## Message Endpoints

### POST `/message`
- Send a message to a channel.
- **Body:**
```json
{
  "sender_id": "john_doe",
  "channel_id": "general",
  "content": "Hello everyone!"
}
```
- **Success Response:**
```json
{
  "message_id": "generated_id",
  "sender_id": "john_doe",
  "channel_id": "general",
  "content": "Hello everyone!"
}
```

### GET `/message/<channel_id>`
- Fetch all messages from a channel.
- **Response:**
```json
[
  {
    "message_id": "generated_id",
    "sender_id": "john_doe",
    "content": "Hello everyone!"
  }
]
```

## Direct Message Endpoints

### POST `/start_dm`
- Start a direct message chat between two users.
- **Body:**
```json
{
  "sender_id": "john_doe",
  "receiver_id": "jane_smith"
}
```
- **Success Response:**
```json
{
  "channel_id": "dm_john_doe_jane_smith"
}
```

---

# 🛠️ CI/CD Pipeline (CircleCI)

CircleCI pipeline automatically runs:

- Static analysis (`mypy`, `ruff`)
- Unit and Integration tests (`pytest`, `nose2`)
- Code coverage check (`coverage --fail-under=70`)

👉️ See `.circleci/config.yml` for full setup.

---

# 📦 Project Structure

```
.
├── app.py
├── src/
│   ├── models/
│   │   ├── __init__.py
│   │   ├── user_model.py
│   │   ├── channel_model.py
│   │   └── message_model.py
│   ├── user/
│   ├── channel/
│   ├── message/
├── tests/
│   ├── integration/
│   ├── e2e/
├── .circleci/
│   └── config.yml
├── pyproject.toml
├── README.md
└── chat.db
```

---

# 📖 Future Improvements

- Add timestamps (`created_at`) for messages.
- Allow editing and deleting messages.
- Add authentication tokens for user sessions.
- Improve models with relational links.
- Add Docker support for easier deployment.

---

# 📉 Quick Commands Cheat Sheet

| Purpose | Command |
|:---|:---|
| Install dependencies | `uv sync --group dev` |
| Initialize database | `flask shell` ➞ `db.create_all()` |
| Start server | `python app.py` |
| Run tests locally | `pytest` |
| Run static analysis | `mypy src/` and `ruff check .` |
| See coverage report | `coverage report -m` |

---

# 🚀 Authors

- Jerry Zou
- Keshav Rajput
- Terry Xu
- Jinglin Tao

---

# 🎉 Happy Chatting!

