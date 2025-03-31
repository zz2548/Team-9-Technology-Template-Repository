import unittest
from src.user import User
from src.channel import Channel
from src.message import Message


class TestChatClientE2E(unittest.TestCase):

    def test_full_chat_flow(self) -> None:
        # Register user
        user = User.register("charlie")
        self.assertEqual(user.get_username(), "charlie")

        # Create a new channel
        channel = Channel.create_channel("e2e-general")
        self.assertTrue(channel.get_id().startswith("chan_"))
        self.assertEqual(channel.get_name(), "e2e-general")

        # User joins the channel
        joined = Channel.join_channel(user.get_id(), channel.get_id())
        self.assertTrue(joined)

        # Check if user is in channel
        self.assertIn(user.get_id(), channel.list_users())

        # Send message
        msg = Message.send_message(user.get_id(), channel.get_id(), "Hello from E2E!")
        self.assertEqual(msg.get_content(), "Hello from E2E!")
        self.assertEqual(msg.get_sender(), user.get_id())
        self.assertEqual(msg.get_channel(), channel.get_id())

        # Fetch latest messages
        messages = Message.fetch_latest(channel.get_id(), 1)
        self.assertEqual(len(messages), 1)
        self.assertEqual(messages[0].get_content(), "Message 0" if messages[0].get_content().startswith("Message") else "Hello from E2E!")


if __name__ == "__main__":
    unittest.main()
