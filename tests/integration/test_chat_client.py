"""
Creates unit tests for the following aspects of the core application logic:
- User creation and login
- Channel creation and user joining
- Message sending and retrieval
All tests assume in-memory behavior.
"""

from src.channel_api import Channel
from src.message_api import Message
from src.user_api import User


def test_user_registration_and_login() -> None:
    """
    Tests the user registration and login process.
    Verifies that a user can successfully register and login and that 
    their username is retrievable.
    """
    
    user = User.register("alice")
    assert user.get_username() == "alice"
    assert isinstance(user, User)

    logged_in = User.login("alice")
    assert logged_in.get_username() == "alice"


def test_channel_creation_and_joining() -> None:
    """
    Tests the channel creation and joining process.
    Verifies that the channel created has a valid name and ID and confirms that
    the user appears in the channel's list.
    """
    
    channel = Channel.create_channel("general")
    assert channel.get_name() == "general"
    assert channel.get_id().startswith("chan_")

    joined = Channel.join_channel("alice_id", channel.get_id())
    assert joined is True

    users = channel.list_users()
    assert "alice_id" in users


def test_message_sending_and_fetching() -> None:
    """
    Tests the message sending and retrieval process.
    Verifies that a message query returns the correct number and type of response.
    """
    
    msg = Message.send_message("alice_id", "chan_1", "Hello world!")
    assert msg.get_content() == "Hello world!"
    assert msg.get_sender() == "alice_id"
    assert msg.get_channel() == "chan_1"

    recent = Message.fetch_latest("chan_1", 3)
    assert len(recent) == 3
    assert all(isinstance(m, Message) for m in recent)
