class Channel:
    def __init__(self, channel_id: str, name: str):
        self.channel_id = channel_id
        self.name = name

    def get_id(self) -> str:
        raise NotImplementedError

    def get_name(self) -> str:
        raise NotImplementedError

    def list_users(self) -> list[str]:
        raise NotImplementedError

    @staticmethod
    def create_channel(name: str) -> 'Channel':
        raise NotImplementedError

    @staticmethod
    def join_channel(user_id: str, channel_id: str):
        raise NotImplementedError
