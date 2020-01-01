from flask_restplus import Namespace, fields


class AuthDto:
    api = Namespace("auth", description="Authentication routes and requests")
    auth_login = api.model(
        "login_details",
        {
            "email": fields.String(required=True, description="User's email"),
            "password": fields.String(required=True, description="User's password"),
        },
    )

    auth_register = api.model(
        "register_data",
        {
            "email": fields.String(
                required=True, description="Email address for logging in."
            ),
            "username": fields.String(
                required=True, description="Username for tagging users."
            ),
            "full_name": fields.String(
                description="Full name for identifying users humanly."
            ),
            "password": fields.String(
                description="Password for securing user accounts."
            ),
            "entry_key": fields.String(
                description="Entry key for registering onto the platform."
            ),
        },
    )
