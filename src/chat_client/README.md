# Discord-like Chat Client - Interface Definition

## Overview

This project defines the public interface for a Discord-like chat client, including:
- User registration & login
- Message exchange
- Channel creation and participation

## Testing

Tests are mocked and located in each module subdirectory:
- `message/test_message.py`
- `user/test_user.py`
- `channel/test_channel.py`

## API Structure

### Message
- `get_id() -> str`
- `get_sender() -> str`
- `get_channel() -> str`
- `get_content() -> str`
- `send_message(sender_id, channel_id, content) -> Message`
- `fetch_latest(channel_id, count) -> list[Message]`

### User
- `get_id() -> str`
- `get_username() -> str`
- `list_channels() -> list[str]`
- `register(username: str) -> User`
- `login(username: str) -> User`

### Channel
- `get_id() -> str`
- `get_name() -> str`
- `list_users() -> list[str]`
- `create_channel(name: str) -> Channel`
- `join_channel(user_id: str, channel_id: str) -> bool`

## ✅ Scope (MVP)

- Text chat in public channels
- User registration and authentication
- Fetching message history per channel

### ❌ Out of Scope
- Private messages
- Emojis & attachments
- Video or voice communication


