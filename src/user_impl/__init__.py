import src.user_api as api

from ._impl import User, UserService

api.get_service = lambda: UserService()
api.User = User
