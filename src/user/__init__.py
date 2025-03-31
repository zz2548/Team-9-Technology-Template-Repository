# Example: user/__init__.py
class User:
    def __init__(self, user_id: str, username: str) -> None:
        self.user_id = user_id
        self.username = username

    def get_id(self) -> str:
        return self.user_id

    def get_username(self) -> str:
        return self.username

    def list_channels(self) -> list[str]:
        return ["general", "random"]

    @staticmethod
    def register(username: str) -> 'User':
        return User("u001", username)

    @staticmethod
    def login(username: str) -> 'User':
        return User("u001", username)
