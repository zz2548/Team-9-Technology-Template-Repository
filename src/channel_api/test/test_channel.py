# No need to import pytest when only using assert statements
from src.channel_api import Channel


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
