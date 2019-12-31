import re

from flask import current_app
from flask_jwt_extended import create_access_token
from datetime import datetime
from uuid import uuid4

from api.main import db
from api.util import Message, ErrResp
from api.main.model.user import User
from api.main.model.schemas import UserSchema

from api.main.service.user_service import load_user

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
                resp = Message(False, "Credentials not fully provided!")
                resp["error_reason"] = "no_credentials"
                return resp, 403

            # Fetch user data
            user = User.query.filter_by(email=email).first()
            if not user:
                resp = Message(
                    False, "The email you have entered does not match any account."
                )
                resp["error_reason"] = "account_404"
                return resp, 404

            elif user and user.check_password(password):
                user_info = load_user(user)
                access_token = create_access_token(identity=user.id)

                if access_token:
                    resp = Message(True, "Logged user in.")
                    resp["Authorization"] = access_token
                    resp["user"] = user_info
                    return resp, 200

            # Return incorrect password if others fail
            resp = Message(False, "Failed to log in, password may be incorrect.")
            resp["error_reason"] = "password_invalid"
            return resp, 403

        except Exception as error:
            current_app.logger.error(error)
            ErrResp()

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
                resp = Message(False, "Email is required!")
                resp["error_reason"] = "email_none"
                return resp, 403

            # Check if the email is being used
            if User.query.filter_by(email=email).first() is not None:
                resp = Message(False, "Email is being used in another account.")
                resp["error_reason"] = "email_used"
                return resp, 403

            # Check if the email is valid
            elif not EMAIl_REGEX.match(email):
                resp = Message(False, "Invalid email!")
                resp["error_reason"] = "email_invalid"
                return resp, 403

            # Check if the username is empty
            if len(username) == 0 or username is None:
                resp = Message(False, "Username is required!")
                resp["error_reason"] = "username_none"
                return resp, 403

            # Check if the username is being used
            elif User.query.filter_by(username=username).first() is not None:
                resp = Message(False, "Username is already taken!")
                resp["error_reason"] = "username_taken"
                return resp, 403

            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                resp = Message(False, "Username length is invalid!")
                resp["error_reason"] = "username_invalid"
                return resp, 403

            # Check if the username is alpha numeric
            elif not username.isalnum():
                resp = Message(False, "Username is not alpha numeric")
                resp["error_reason"] = "username_not_alphanum"
                return resp, 403

            # Verify the full name and if it exists
            if len(full_name) == 0 or full_name is None:
                full_name = None

            else:
                # Validate the full name
                # Remove any spaces so that it properly checks.
                if not full_name.replace(" ", "").isalpha():
                    resp = Message(False, "Name is not alphabetical!")
                    resp["error_reason"] = "name_not_alpha"
                    return resp, 403

                # Check if the full name is equal to or between 2 and 50
                elif not 2 <= len(full_name) <= 50:
                    resp = Message(False, "Name length is invalid")
                    resp["error_reason"] = "name_invalid"
                    return resp, 403

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
            ErrResp()
