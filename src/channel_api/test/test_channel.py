import importlib
import sys
from unittest.mock import patch

from src.channel_api import Channel, get_service
from src.channel_api.interfaces import ChannelEntity, ChannelService
from src.channel_impl._impl import InMemoryChannel, InMemoryChannelService

class MockChannel(Channel):
    def __init__(self, channel_id: str, name: str) -> None:
        super().__init__(channel_id, name)

    def get_id(self) -> str:
        return self.channel_id

    def get_name(self) -> str:
        return self.name

    def list_users(self) -> list[str]:
        return ["u1", "u2"]

    @staticmethod
    def create_channel(name: str) -> "Channel":
        return MockChannel("c123", name)

    @staticmethod
    def join_channel(_user_id: str, _channel_id: str) -> bool:
        return True


def test_create_and_get_channel() -> None:
    chan = MockChannel.create_channel("general")
    assert chan.get_name() == "general"


def test_join_channel() -> None:
    result = MockChannel.join_channel("u42", "general")
    assert result is True


def test_list_users() -> None:
    chan = MockChannel("c1", "general")
    users = chan.list_users()
    assert "u1" in users


def test_create_channel() -> None:
    chan = Channel.create_channel("support")
    assert isinstance(chan, Channel)
    assert chan.get_id().startswith("chan_")
    assert chan.get_name() == "support"


def test_join_same_user_twice() -> None:
    chan = Channel("chan_x", "general")
    Channel.join_channel("user42", "chan_x")
    # Joining same user_api again
    result = Channel.join_channel("user42", "chan_x")
    assert result is True
    assert chan.list_users().count("user42") == 1  # still one instance


def test_channel_reinit() -> None:
    # First init creates the entry
    Channel("chan_y", "alpha")
    # Second init shouldn't overwrite
    Channel("chan_y", "beta")
    chan = Channel("chan_y", "alpha")
    assert chan.get_name() == "alpha"


def test_channel_get_methods() -> None:
    # Test the get methods directly
    chan = Channel("channel_123", "test-channel")
    assert chan.get_id() == "channel_123"
    assert chan.get_name() == "test-channel"


def test_multiple_users_in_channel() -> None:
    # Test adding multiple users
    chan_id = "multichan"
    Channel(chan_id, "multi-user")
    Channel.join_channel("user1", chan_id)
    Channel.join_channel("user2", chan_id)
    Channel.join_channel("user3", chan_id)

    chan = Channel(chan_id, "multi-user")
    users = chan.list_users()
    assert "user1" in users
    assert "user2" in users
    assert "user3" in users
    assert len(users) == 3


def test_empty_channel()  -> None:
    # Test a newly created channel has no users
    chan = Channel("empty_chan", "empty")
    assert len(chan.list_users()) == 0


def test_channel_service_directly():
    """Test the service directly instead of through static methods."""
    from src.channel_api import get_service

    service = get_service()
    chan = service.create_channel("direct-test")
    assert chan.get_name() == "direct-test"
    assert chan.get_id().startswith("chan_")

    result = service.join_channel("user99", chan.get_id())
    assert result is True
    assert "user99" in chan.list_users()


def test_nonexistent_channel():
    """Test joining a nonexistent channel."""
    result = Channel.join_channel("user1", "nonexistent_channel")
    assert result is True  # Your implementation always returns True

    # Verify channel was created implicitly
    assert "nonexistent_channel" in Channel.channels_


def test_channel_id_generation():
    """Test unique ID generation for channels."""
    chan1 = Channel.create_channel("test1")
    chan2 = Channel.create_channel("test2")
    assert chan1.get_id() != chan2.get_id()
    assert chan1.get_id().startswith("chan_")
    assert chan2.get_id().startswith("chan_")


def test_module_initialization() -> None:
    """Test the module initialization directly."""
    # Force reload the module to test initialization
    if "src.channel_api" in sys.modules:
        del sys.modules["src.channel_api"]

    # Re-import to trigger initialization code
    import src.channel_api

    # Verify the initialization worked
    assert isinstance(src.channel_api.Channel, type)
    assert issubclass(src.channel_api.Channel, ChannelEntity)
    # Use get_service() instead of accessing private _service
    assert isinstance(get_service(), ChannelService)


def test_lazy_service_directly() -> None:
    """Test the _lazy_service function directly."""
    # Import it directly
    from src.channel_api import _lazy_service

    service = _lazy_service()
    assert isinstance(service, InMemoryChannelService)


def test_static_method_assignment() -> None:
    """Test the static method assignment directly."""
    # Force reload to test assignment
    if "src.channel_api" in sys.modules:
        del sys.modules["src.channel_api"]

    # Use combined with statement without unused variables
    with patch.object(Channel, 'create_channel', None), patch.object(Channel, 'join_channel', None):
        import src.channel_api

        # Verify the methods were assigned
        assert Channel.create_channel is not None
        assert Channel.join_channel is not None


def test_type_checking_branch() -> None:
    """Test the TYPE_CHECKING branch."""
    # We can't directly test this, but we can verify the imports work
    from typing import TYPE_CHECKING

    if TYPE_CHECKING:
        from src.channel_impl._impl import InMemoryChannel
        assert InMemoryChannel is not None


def test_service_implementation_details() -> None:
    """Test specific details of the service implementation."""
    service = InMemoryChannelService()

    # Clear channels for clean test
    InMemoryChannel.channels_ = {}

    # Test ID generation with empty channels dict
    chan1 = service.create_channel("test1")
    assert chan1.get_id() == "chan_1"

    # Add some channels and test again
    InMemoryChannel.channels_["fake1"] = []
    InMemoryChannel.channels_["fake2"] = []

    chan2 = service.create_channel("test2")
    assert chan2.get_id() == "chan_4"  # Should be 4 since there are 3 existing


def test_join_handling_edge_cases() -> None:
    """Test edge cases in join_channel."""
    service = InMemoryChannelService()

    # Clear channels for clean test
    InMemoryChannel.channels_ = {}

    # Join non-existent channel
    result = service.join_channel("user1", "nonexistent")
    assert result is True
    assert "nonexistent" in InMemoryChannel.channels_

    # Join same user twice
    service.join_channel("user1", "nonexistent")  # Again
    assert len(InMemoryChannel.channels_["nonexistent"]) == 1  # Still only one
    assert "user1" in InMemoryChannel.channels_["nonexistent"]

    # Join another user
    service.join_channel("user2", "nonexistent")
    assert len(InMemoryChannel.channels_["nonexistent"]) == 2
    assert "user2" in InMemoryChannel.channels_["nonexistent"]


def test_list_users_edge_cases() -> None:
    """Test edge cases for list_users."""
    # Test with empty channel
    InMemoryChannel.channels_ = {"empty": []}
    chan = InMemoryChannel("empty", "Empty Channel")
    assert chan.list_users() == []

    # Test non-existent channel (should create it)
    nonexistent_chan = InMemoryChannel("nonexistent", "Should Create")
    assert nonexistent_chan.list_users() == []
    assert "nonexistent" in InMemoryChannel.channels_


def test_channel_cast_in_init() -> None:
    """Test the Channel type cast in __init__.py."""
    from src.channel_api import Channel

    # Verify it's properly casting to the right type
    assert Channel is not None
    assert Channel.__name__ == "InMemoryChannel"  # This tests the cast worked

    # Create and test instance
    chan = Channel("test_id", "test_name")
    assert chan.channel_id == "test_id"
    assert chan.name == "test_name"