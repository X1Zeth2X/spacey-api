# User service utils.

from api.util import Message, ErrResp

from api.main.model.user import User
from api.main.model.schemas import UserSchema

private_info = (
    "password_hash",
    "id",
)

# Define deserializer
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
    info = user_schema.dump(user_obj)

    # Filter
    filter_user(info)

    return info
