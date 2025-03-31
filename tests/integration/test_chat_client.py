import unittest
from chat_client.user import User
from chat_client.channel import Channel
from chat_client.message import Message


class TestChatClientIntegration(unittest.TestCase):

    def test_user_registration_and_login(self) -> None:
        user = User.register("alice")
        self.assertEqual(user.get_username(), "alice")
        self.assertIsInstance(user, User)

        logged_in = User.login("alice")
        self.assertEqual(logged_in.get_username(), "alice")

    def test_channel_creation_and_joining(self) -> None:
        channel = Channel.create_channel("general")
        self.assertEqual(channel.get_name(), "general")
        self.assertTrue(channel.get_id().startswith("chan_"))

        joined = Channel.join_channel("alice_id", channel.get_id())
        self.assertTrue(joined)

        users = channel.list_users()
        self.assertIn("alice_id", users)

    def test_message_sending_and_fetching(self) -> None:
        msg = Message.send_message("alice_id", "chan_1", "Hello world!")
        self.assertEqual(msg.get_content(), "Hello world!")
        self.assertEqual(msg.get_sender(), "alice_id")
        self.assertEqual(msg.get_channel(), "chan_1")

        recent = Message.fetch_latest("chan_1", 3)
        self.assertEqual(len(recent), 3)
        self.assertTrue(all(isinstance(m, Message) for m in recent))


if __name__ == '__main__':
    unittest.main()
