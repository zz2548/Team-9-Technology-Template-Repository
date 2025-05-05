# Chat Client API 

This project implements a basic **chat client server** in Python using **Flask** and **SQLite**.  
It provides RESTful APIs for:

- User registration and login
- Token based authentication
- Creating and joining chat channels
- Sending and fetching messages
- Direct messaging between two users
- **AI chatbot integration** powered by the external `ai_convo_client` module using GIT Submodules
- **Issuer tracker integration** powered by the external `issuer_tracker` module using GIT Submodules


# Features

- **Register** new users (UUID-based IDs)
- **Login** existing users
- **Create Channels**
- **Join Channels**
- **Send Messages** to channels
- **Fetch Messages** from channels
- **Start Direct Messages** between two users
- **Chat with AI bot** in dedicated `ai-helpdesk` channel
- **Persistent database** using SQLite

# Cloning the project
```bash
git clone https://github.com/zz2548/Team-9-Technology-Template-Repository.git

git submodule update --init --recursive

```

# Running the Server

## Setup environment

```bash
# On Linux/macOS
export FLASK_APP=app.py

# On Windows PowerShell
$env:FLASK_APP = "app.py"

# On Windows Command Prompt
set FLASK_APP=app.py
```
## Initialize the database
```bash
# Create database tables
flask init-db

# Create AI bot user
flask seed-ai-bot
```
## Start the server
```bash
# Option 1: Using Flask run command
flask run

# Option 2: Using Python directly
python app.py
```
## Additional commands
```bash
# Drop all database tables (will prompt for confirmation)
flask drop-db

# Then recreate them
flask init-db
flask seed-ai-bot
```

Server will run at: `http://127.0.0.1:5000/`

# Frontend UI
The UI provides a user-friendly interface for:
- Registering and logging in users
- Token based authentication and logging out users
- Creating and joining channels
- Sending and receiving messages
- Chatting with the AI bot in the ai-helpdesk channel

## Screenshot
![image](https://github.com/user-attachments/assets/11e617d4-9037-4efd-9d11-a976b815c6e7)

# Integration Tests
Integration tests are located under the tests/integration/ directory.
Tested scenarios include:

- User registration and login flows
- Token based authentication
- Channel creation and joining
- Sending and receiving messages
- AI bot interaction through ai-helpdesk channel
- Direct messaging between two users

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
  "user_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
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
  "user_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
  "username": "john_doe"
}
```

## Channel Endpoints

### POST `/channel`
- Create a new chat channel.
- **Body:**
```json
{
  "name": "ai-helpdesk"
}
```
- **Success Response:**
```json
{
  "channel_id": "55352752-b3c0-4c60-8dbe-ec02589448f9",
  "name": "ai-helpdesk"
}
```

### POST `/channel/join`
- Join an existing channel.
- **Body:**
```json
{
  "user_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
  "channel_id": "55352752-b3c0-4c60-8dbe-ec02589448f9"
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
  "users": ["f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2"]
}
```

## Message Endpoints

### POST `/message`
- Send a message to a channel. If the channel name is `ai-helpdesk`, the message will trigger a response from the integrated AI bot via `ai_convo_client`.
- **Body:**
```json
{
  "sender_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
  "channel_id": "55352752-b3c0-4c60-8dbe-ec02589448f9",
  "content": "Hello AI!"
}
```
- **Success Response:**
```json
[
  {
    "message_id": "msg_id_1",
    "sender_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
    "channel_id": "55352752-b3c0-4c60-8dbe-ec02589448f9",
    "content": "Hello AI!"
  },
  {
    "message_id": "msg_id_2",
    "sender_id": "ai_bot",
    "channel_id": "55352752-b3c0-4c60-8dbe-ec02589448f9",
    "content": "Hi! How can I assist you today?"
  }
]
```

### GET `/message/<channel_id>`
- Fetch all messages from a channel.
- **Response:**
```json
[
  {
    "message_id": "55352752-b3c0-4c60-8dbe-ec02589448f9",
    "sender_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
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
  "sender_id": "f4c9a64a-6b02-4980-b29a-5dfd7e59f3c2",
  "receiver_id": "another_user_uuid"
}
```
- **Success Response:**
```json
{
  "channel_id": "dm_f4c9a64a_another_user"
}
```

# Future Improvements

- Add timestamps (`created_at`) for messages.
- Allow editing and deleting messages.
- Improve models with relational links.
- Add Docker support for easier deployment.
- Persist conversation history for AI bot
- Enhance AI response accuracy with additional context

---

# Authors

- Jerry Zou
- Keshav Rajput
- Terry Mu
- Jinglin Tao
- Mahin Lalani
