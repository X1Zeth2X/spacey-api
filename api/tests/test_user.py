import unittest
import json

from flask import current_app
from api.tests.base import BaseTestCase
from api.tests.common import register_user, login_user


def get_user(self, access_token, username):
    return self.client.get(
        f"/user/get/{username}",
        headers={f"Authorization": "Bearer {access_token}"},
        content_type="application/json",
    )


class TestAuthBlueprint(BaseTestCase):
    def test_registered_user_login(self):
        """ Test for login of registered-user login """

        with self.client:
            # User registration
            user_response = register_user(self)
            response_data = json.loads(user_response.data.decode())

            self.assertEqual(user_response.status_code, 201)

            # Registered user login
            login_response = login_user(self)
            data = json.loads(login_response.data.decode())

            self.assertTrue(data["Authorization"])
            self.assertEqual(login_response.status_code, 200)

    def test_get_user(self):
        """ Get a specific user using its username """

        with self.client:
            # User registration
            register_user(self)
            login_response = login_user(self)
            login_response_data = json.loads(login_response.data.decode())
            access_token = login_response_data["Authorization"]

            # Get the user data
            username = login_response_data["user"]["username"]
            get_response = get_user(self, access_token, username)
            get_response_data = json.loads(get_response.data.decode())

            self.assertEqual(get_response.status_code, 200)


if __name__ == "__main__":
    unittest.main()
