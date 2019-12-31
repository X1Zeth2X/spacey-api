## Main User Service

from api.util import Message
from .utils import get_user, load_user


class UserService:
    # Get user info by its username
    @staticmethod
    def get_user_info(username):
        user_obj = get_user(username)
        user_info = load_user(user_obj)

        resp = Message(True, "user data sent.")
        resp["user"] = user_info
        return resp, 200
