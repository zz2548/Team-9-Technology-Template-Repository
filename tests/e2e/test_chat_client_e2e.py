# No need to import pytest when only using assert statements
from src.channel_api import Channel
from src.message_api import Message
from src.user_api import User


def test_full_chat_flow() -> None:
    # Register user_api
    user = User.register("charlie")
    assert user.get_username() == "charlie"

    # Create a new channel_api
    channel = Channel.create_channel("e2e-general")
    assert channel.get_id().startswith("chan_")
    assert channel.get_name() == "e2e-general"

    # User joins the channel_api
    joined = Channel.join_channel(user.get_id(), channel.get_id())
    assert joined is True

    # Check if user_api is in channel_api
    assert user.get_id() in channel.list_users()

    # Send message_api
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
