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


class FactDto:
    api = Namespace("fact", description="Fact related operations.")
    create_fact = api.model(
        "payload",
        {
            "planet": fields.String(required=True, description="Planet's name."),
            "title": fields.String(required=True, description="Fact title."),
            "content": fields.String(required=True, description="Fact content."),
        },
    )

class FactsDto:
    api = Namespace("facts", description="Route for getting facts information.")