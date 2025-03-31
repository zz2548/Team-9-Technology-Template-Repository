# Team-9-Technology-Template-Repository

# Chat Client – Discord-Style

This project is a modular chat client inspired by Discord, designed as part of a software engineering coursework assignment. It focuses on defining clean interfaces between components and writing robust tests for those interfaces.


## Interface Summary

### `User`
- `register(username: str) -> User`
- `login(username: str) -> User`
- `get_id() -> str`
- `get_username() -> str`
- `list_channels() -> list[str]`

### `Channel`
- `create_channel(name: str) -> Channel`
- `join_channel(user_id: str, channel_id: str) -> bool`
- `get_id() -> str`
- `get_name() -> str`
- `list_users() -> list[str]`

### `Message`
- `send_message(sender_id: str, channel_id: str, content: str) -> Message`
- `fetch_latest(channel_id: str, count: int) -> list[Message]`
- `get_id() -> str`
- `get_sender() -> str`
- `get_channel() -> str`
- `get_content() -> str`

> Each module is defined using class-based interfaces with static methods for construction or querying.

## Scope of Work

### In Scope
- Basic interface definitions with trivial logic
- Mockable methods for future implementation
- Type-safe method signatures using Python type hints
- Full test coverage across:
  - Unit tests (via `nose2`)
  - Integration tests
  - End-to-end user simulations

### Out of Scope
- No actual networking or persistent storage
- No authentication or encryption
- No UI/Frontend



