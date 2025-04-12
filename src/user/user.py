import uuid
from typing import List, Dict, Optional

# In-memory storage for users
_users_by_id: Dict[str, 'User'] = {}
_users_by_username: Dict[str, 'User'] = {}


class User:
    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username
        self.channels: List[str] = ["general", "random"]  # Default channels

        # Store user in memory
        _users_by_id[self.user_id] = self
        _users_by_username[self.username] = self

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> List[str]:
        return self.channels

    def join_channel(self, channel_name: str) -> None:
        """Add a channel to the user's channel list if not already joined."""
        if channel_name not in self.channels:
            self.channels.append(channel_name)

    def leave_channel(self, channel_name: str) -> bool:
        """Remove a channel from the user's channel list.
        Returns True if the channel was removed, False if not found.
        """
        if channel_name in self.channels:
            self.channels.remove(channel_name)
            return True
        return False

    def to_dict(self) -> Dict:
        """Convert user to dictionary for JSON serialization."""
        return {
            "id": self.user_id,
            "username": self.username,
            "channels": self.channels
        }

    @staticmethod
    def register(username: str) -> Optional['User']:
        """Register a new user with the given username.
        Returns None if the username is already taken.
        """
        if username in _users_by_username:
            return None

        # Generate a unique user ID
        user_id = str(uuid.uuid4())
        return User(user_id, username)

    @staticmethod
    def login(username: str) -> Optional['User']:
        """Login a user with the given username.
        Returns None if the username doesn't exist.
        """
        return _users_by_username.get(username)

    @staticmethod
    def get_by_id(user_id: str) -> Optional['User']:
        """Get a user by their ID.
        Returns None if the user ID doesn't exist.
        """
        return _users_by_id.get(user_id)

    @staticmethod
    def get_all_users() -> List['User']:
        """Get a list of all registered users."""
        return list(_users_by_id.values())


# Create some default users for testing
if not _users_by_id:
    User("u001", "alice")
    User("u002", "bob")
    User("u003", "charlie")