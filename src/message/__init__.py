class Message:
    def __init__(self, sender_id: str, channel_id: str, content: str) -> None:
        self.sender_id = sender_id
        self.channel_id = channel_id
        self.content = content

    def get_id(self) -> str:
        raise NotImplementedError

    def get_sender(self) -> str:
        raise NotImplementedError

    def get_channel(self) -> str:
        raise NotImplementedError

    def get_content(self) -> str:
        raise NotImplementedError

    @staticmethod
    def send_message(sender_id: str, channel_id: str, content: str) -> 'Message':
        raise NotImplementedError

    @staticmethod
    def fetch_latest(channel_id: str, count: int) -> list['Message']:
        raise NotImplementedError
