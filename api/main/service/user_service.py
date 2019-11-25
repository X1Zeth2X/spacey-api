## User Service

from datetime import datetime

from api.main import db
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
        response_object = {
            "success": False,
            "message": "User does not exist!",
            "error_reason": "non_existent",
        }
        return response_object, 404

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

        response_object = {
            "success": True,
            "message": "User data sent.",
            "user": user_info,
        }
        return response_object, 200
