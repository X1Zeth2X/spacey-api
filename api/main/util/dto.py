from flask_restplus import Namespace, fields


class UserDto:
    api = Namespace("user", description="User related operations.")
    user = api.model(
        "user",
        {
            "email": fields.String(required=True, description="User's email address"),
            "username": fields.String(required=True, description="User's username"),
            "full_name": fields.String(description="User's full name"),
            "password": fields.String(required=True, description="User's password"),
        },
    )
