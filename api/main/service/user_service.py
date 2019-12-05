## User Service

from datetime import datetime

from api.main import db
from api.util import Message, ErrResp
from ..model.users import User, UserSchema

private_info = (
    "password_hash",
    "id",
)

# Define schema
user_schema = UserSchema()

# You can use either an ID or Username
def get_user(identifier):
    if type(identifier) == int:
        user = User.query.filter_by(id=identifier).first()
    else:
        user = User.query.filter_by(username=identifier).first()

    if not user:
        resp = Message(False, "User does not exist!")
        resp["error_reason"] = "user_404"
        return resp, 404

    return user


def filter_user(user):
    # Remove sensitive information
    for i in private_info:
        del user[i]

    return user


def load_user(user_obj):
    user_info = user_schema.dump(user_obj)

    # Filter
    filter_user(user_info)

    return user_info


class UserService:
    # Get user info by its username
    def get_user_info(username):
        user_obj = get_user(username)
        user_info = load_user(user_obj)

        resp = Message(True, "user data sent.")
        resp["user"] = user_info
        return resp, 200
