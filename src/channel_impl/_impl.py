from typing import ClassVar

from src.channel_api.interfaces import ChannelEntity, ChannelService


class InMemoryChannel(ChannelEntity):
    """
    An in-memory representation of a communication channel.

    This class simulates a basic channel entity by tracking users in a shared class dictionary.
    All instances share the same state through 'channels_'.
    """
    
    channels_: ClassVar[dict[str, list[str]]] = {}

    def __init__(self, channel_id: str, name: str) -> None:
        """Initializes a new in-memory channel and adds it to the shared channel store."""
        
        self.channel_id = channel_id
        self.name = name
        self.channels_.setdefault(channel_id, [])

    def get_id(self) -> str:
        """Returns the channel's unique id."""
        
        return self.channel_id

    def get_name(self) -> str:
        """Returns the channel's name."""
        
        return self.name

    def list_users(self) -> list[str]:
        """Returns a list of all users in the channel."""
        
        return self.channels_[self.channel_id]

class InMemoryChannelService(ChannelService):
    """
    A service class for managing in memory channels.

    This class provides operations for creating channels and allowing users to join them.
    """
    
    def create_channel(self, name: str) -> ChannelEntity:
        """Creates a new, in-memory, channel with a unique id."""
        
        new_id = f"chan_{len(InMemoryChannel.channels_) + 1}"
        return InMemoryChannel(new_id, name)

    def join_channel(self, user_id: str, channel_id: str) -> bool:
        """Adds a user to a specified channel if they are not already a member."""
        
        InMemoryChannel.channels_.setdefault(channel_id, [])
        if user_id not in InMemoryChannel.channels_[channel_id]:
            InMemoryChannel.channels_[channel_id].append(user_id)
        return True
