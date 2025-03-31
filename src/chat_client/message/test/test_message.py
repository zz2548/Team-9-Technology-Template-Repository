import unittest
from chat_client.message import Message

class MockMessage(Message):
    def get_id(self):
        return "msg001"
    
    def get_sender(self):
        return self.sender_id

    def get_channel(self):
        return self.channel_id

    def get_content(self):
        return self.content

    @staticmethod
    def send_message(sender_id, channel_id, content):
        return MockMessage(sender_id, channel_id, content)

    @staticmethod
    def fetch_latest(channel_id, count):
        return [MockMessage("u1", channel_id, f"msg {i}") for i in range(count)]

class TestMessageAPI(unittest.TestCase):
    def test_send_and_get_message(self):
        msg = MockMessage.send_message("u42", "general", "Hello!")
        self.assertEqual(msg.get_sender(), "u42")
        self.assertEqual(msg.get_channel(), "general")
        self.assertEqual(msg.get_content(), "Hello!")

    def test_fetch_latest(self):
        msgs = MockMessage.fetch_latest("general", 3)
        self.assertEqual(len(msgs), 3)
        self.assertTrue(all(isinstance(m, MockMessage) for m in msgs))

if __name__ == '__main__':
    unittest.main()
