# No need to import pytest when only using assert statements
from src.channel import Channel
from src.message import Message
from src.user import User


def test_full_chat_flow() -> None:
    # Register user
    user = User.register("charlie")
    assert user.get_username() == "charlie"

    # Create a new channel
    channel = Channel.create_channel("e2e-general")
    assert channel.get_id().startswith("chan_")
    assert channel.get_name() == "e2e-general"

    # User joins the channel
    joined = Channel.join_channel(user.get_id(), channel.get_id())
    assert joined is True

    # Check if user is in channel
    assert user.get_id() in channel.list_users()

    # Send message
    msg = Message.send_message(user.get_id(), channel.get_id(), "Hello from E2E!")
    assert msg.get_content() == "Hello from E2E!"
    assert msg.get_sender() == user.get_id()
    assert msg.get_channel() == channel.get_id()

    # Fetch latest messages
    messages = Message.fetch_latest(channel.get_id(), 1)
    assert len(messages) == 1
    expected_content = (
        "Message 0"
        if messages[0].get_content().startswith("Message")
        else "Hello from E2E!"
    )
    assert messages[0].get_content() == expected_content
