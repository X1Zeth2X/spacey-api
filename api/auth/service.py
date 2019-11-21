import re

from flask import current_app
from flask_jwt_extended import create_access_token
from datetime import datetime
from uuid import uuid4

from api.main import db
from api.main.model.users import User, UserSchema

# Basic email regex.
# For more security, use a more complex regex.
EMAIl_REGEX = re.compile(r"[^@]+@[^@]+\.[^@]+")

class AuthService:
    @staticmethod
    def login_user(data):
        # Assign the vars
        email = data["email"]
        password = data["password"]

        try:
            # Check if the email or password was provided
            if not email or not password:
                response_object = {
                    "success": False,
                    "message": "Credentials not fully provided!",
                    "error_reason": "no_credentials",
                }
                return response_object, 403

            # Fetch user data
            user = User.query.filter_by(email=email).first()
            if not user:
                response_object = {
                    "success": False,
                    "message": "The email you have entered does not match any account.",
                    "error_reason": "no_account",
                }
                return response_object, 404
            
            elif user and user.check_password(password):
                pass

            # Return incorrect password if others fail
            response_object = {
                "success": False,
                "message": "Failed to log in, password may be incorrect.",
                "error_reason": "invalid_password",
            }
            return response_object, 403

        except Exception as error:
            # Log error
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_failed",
            }
            return response_object, 500