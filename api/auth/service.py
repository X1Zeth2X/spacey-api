import re

from flask import current_app
from flask_jwt_extended import create_access_token
from datetime import datetime
from uuid import uuid4

from api.main import db
from api.util import Message, InternalErrResp, ErrResp
from api.main.model.user import User
from api.main.model.schemas import UserSchema

from api.main.service.user.utils import load_user

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
                ErrResp("Credentials not fully provided!", "invalid_credentials", 400)

            # Fetch user data
            user = User.query.filter_by(email=email).first()
            if not user:
                ErrResp(
                    "The email you have entered does not match any account.",
                    "account_404",
                    404,
                )

            elif user and user.check_password(password):
                user_info = load_user(user)
                access_token = create_access_token(identity=user.id)

                if access_token:
                    resp = Message(True, "Logged user in.")
                    resp["Authorization"] = access_token
                    resp["user"] = user_info
                    return resp, 200

            # Return incorrect password if others fail
            ErrResp(
                "Failed to login, password may be incorrect.", "invalid_password", 403
            )

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()

    @staticmethod
    def register(data):
        try:
            # Assign the vars
            email = data["email"]
            username = data["username"]
            full_name = data["full_name"]
            password = data["password"]

            # Check if email exists
            if len(email) == 0 or email is None:
                ErrResp("Email is required!", "invalid_email", 400)

            # Check if the email is being used
            if User.query.filter_by(email=email).first() is not None:
                ErrResp("Email is used by another account.", "email_used", 403)

            # Check if the email is valid
            elif not EMAIl_REGEX.match(email):
                ErrResp("Invalid email!", "email_invalid", 400)

            # Check if the username is empty
            if len(username) == 0 or username is None:
                ErrResp("Username is required!", "invalid_username", 400)

            # Check if the username is being used
            elif User.query.filter_by(username=username).first() is not None:
                ErrResp("Username is already taken!", "username_taken", 403)

            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                ErrResp("Username length is invalid!", "invalid_username", 400)

            # Check if the username is alpha numeric
            elif not username.isalnum():
                ErrResp("Username is not alpha numeric.", "username_not_alphanum", 400)

            # Verify the full name and if it exists
            if len(full_name) == 0 or full_name is None:
                full_name = None

            else:
                # Validate the full name
                # Remove any spaces so that it properly checks.
                if not full_name.replace(" ", "").isalpha():
                    ErrResp("Name is not alphabetical.", "invalid_name", 400)

                # Check if the full name is equal to or between 2 and 50
                elif not 2 <= len(full_name) <= 50:
                    ErrResp("Name length is invalid.", "invalid_name", 400)

                # Replace multiple spaces with one.
                # 'firstName    lastName' -> 'firstName lastName'
                re.sub(" +", " ", full_name)

            # Create new user object
            new_user = User(
                email=email,
                username=username,
                full_name=full_name,
                password=password,
                joined_date=datetime.utcnow(),
            )

            # Add and commit the user to the database
            db.session.add(new_user)
            db.session.flush()

            # Get the user's info
            user_info = load_user(new_user)

            # Save changes
            db.session.commit()

            # Return success response
            access_token = create_access_token(identity=new_user.id)

            resp = Message(True, "User has been registered.")
            resp["Authorization"] = access_token
            resp["user"] = user_info
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            InternalErrResp()
