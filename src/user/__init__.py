from typing import List

class User:
    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    def get_id(self) -> str:
        raise NotImplementedError

    def get_username(self) -> str:
        raise NotImplementedError

    def list_channels(self) -> List[str]:
        raise NotImplementedError

    @staticmethod
    def register(username: str) -> 'User':
        raise NotImplementedError

    @staticmethod
    def login(username: str) -> 'User':
        raise NotImplementedError
