"""
Channel API module initialization.
Provides interfaces and implementations for the channel service.
"""
from typing import TYPE_CHECKING, cast

# Import interfaces at the top level for better organization
from .interfaces import ChannelEntity, ChannelService

# Import implementation directly at module level instead of using aliases with *
from src.channel_impl._impl import InMemoryChannel as ChannelImpl

# Type checking imports - correctly formatted
if TYPE_CHECKING:
    from src.channel_impl._impl import InMemoryChannel  # noqa: F401

# Decide on a single approach - either lazy loading or not
# Option 1: Direct import (no lazy loading)
from src.channel_impl._impl import InMemoryChannelService

# Initialize service directly
service: ChannelService = InMemoryChannelService()


def get_service() -> ChannelService:
    """Get the channel service instance."""
    return service


# Define Channel type with proper casting
Channel: type[ChannelEntity] = cast(type[ChannelEntity], ChannelImpl)


def create(name: str) -> ChannelEntity:
    """Create a new channel with the given name.

    Args:
        name: The name of the channel to create

    Returns:
        The newly created channel entity
    """
    return get_service().create_channel(name)


def join(user_id: str, channel_id: str) -> bool:
    """Join a user to a channel.

    Args:
        user_id: The ID of the user joining the channel
        channel_id: The ID of the channel to join

    Returns:
        True if the join operation was successful, False otherwise
    """
    return get_service().join_channel(user_id, channel_id)


# Attach static methods to Channel class
Channel.create_channel = staticmethod(create)  # type: ignore[attr-defined]
Channel.join_channel = staticmethod(join)  # type: ignore[attr-defined]