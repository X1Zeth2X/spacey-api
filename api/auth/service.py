import re

from flask import current_app
from flask_jwt_extended import create_access_token
from datetime import datetime
from uuid import uuid4

from api.main import db
from api.main.model.users import User, UserSchema

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
                user_info = load_user(user)
                access_token = create_access_token(identity=user.id)

                if access_token:
                    response_object = {
                        "success": True,
                        "message": "Successfully logged in.",
                        "Authorization": access_token,
                        "user": user_info,
                    }
                    return response_object, 200

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
                response_object = {
                    "success": False,
                    "message": "Email is required!",
                    "error_reason": "no_email",
                }
                return response_object, 403

            # Check if the email is being used
            if User.query.filter_by(email=email).first() is not None:
                response_object = {
                    "success": False,
                    "message": "Email is being used in another account.",
                    "error_reason": "email_used",
                }
                return response_object, 403

            # Check if the email is valid
            elif not EMAIl_REGEX.match(email):
                response_object = {
                    "success": False,
                    "message": "Invalid email!",
                    "error_reason": "email_invalid",
                }
                return response_object, 403

            # Check if the username is empty
            if len(username) == 0 or username is None:
                response_object = {
                    "success": False,
                    "message": "Username is required!",
                    "error_reason": "no_username",
                }
                return response_object, 403

            # Check if the username is being used
            elif User.query.filter_by(username=username).first() is not None:
                response_object = {
                    "success": False,
                    "message": "Username is already taken!",
                    "error_reason": "username_taken",
                }
                return response_object, 403

            # Check if the username is equal to or between 4 and 15
            elif not 4 <= len(username) <= 15:
                response_object = {
                    "success": False,
                    "message": "Username length is invalid!",
                    "error_reason": "username_invalid",
                }
                return response_object, 403

            # Check if the username is alpha numeric
            elif not username.isalnum():
                response_object = {
                    "success": False,
                    "message": "Username is not alpha numeric",
                    "error_reason": "username_not_alpha_numeric",
                }
                return response_object, 403

            # Verify the full name and if it exists
            if len(full_name) == 0 or full_name is None:
                full_name = None

            else:
                # Validate the full name
                # Remove any spaces so that it properly checks.
                if not full_name.replace(" ", "").isalpha():
                    response_object = {
                        "success": False,
                        "message": "Name is not alphabetical!",
                        "error_reason": "fullname_notalpha",
                    }
                    return response_object, 403

                # Check if the full name is equal to or between 2 and 50
                elif not 2 <= len(full_name) <= 50:
                    response_object = {
                        "success": False,
                        "message": "Name is length is invalid!",
                        "error_reason": "fullname_invalid!",
                    }
                    return response_object, 403

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
            response_object = {
                "success": True,
                "message": "User has successfully been registered.",
                "Authorization": access_token,
                "user": user_info,
            }
            return response_object, 201

        except Exception as error:
            print(error)
            response_object = {
                "success": False,
                "message": "Something went wrong during the process!",
                "error_reason": "server_error",
            }
            return response_object, 500
