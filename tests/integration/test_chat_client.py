# No need to import pytest when only using assert statements
from src.channel_api import Channel
from src.message import Message
from src.user import User


def test_user_registration_and_login() -> None:
    user = User.register("alice")
    assert user.get_username() == "alice"
    assert isinstance(user, User)

    logged_in = User.login("alice")
    assert logged_in.get_username() == "alice"


def test_channel_creation_and_joining() -> None:
    channel = Channel.create_channel("general")
    assert channel.get_name() == "general"
    assert channel.get_id().startswith("chan_")

    joined = Channel.join_channel("alice_id", channel.get_id())
    assert joined is True

    users = channel.list_users()
    assert "alice_id" in users


def test_message_sending_and_fetching() -> None:
    msg = Message.send_message("alice_id", "chan_1", "Hello world!")
    assert msg.get_content() == "Hello world!"
    assert msg.get_sender() == "alice_id"
    assert msg.get_channel() == "chan_1"

    recent = Message.fetch_latest("chan_1", 3)
    assert len(recent) == 3
    assert all(isinstance(m, Message) for m in recent)
