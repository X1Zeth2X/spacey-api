from flask import request
from flask_restplus import Resource

from api.main import limiter
from .util.dto import AuthDto
from .service import AuthService

api = AuthDto.api
auth_login = AuthDto.auth_login
auth_register = AuthDto.auth_register


@api.route("/login")
class AuthLogin(Resource):
    """ User login route
    Client sends user login data and receives an access token.
    """

    @api.doc("Authentication login route")
    @api.expect(auth_login, validate=True)
    def post(self):
        """ Login using email and password """
        # Grab the login data
        login_data = request.get_json()
        return AuthService.login_user(login_data)


@api.route("/register")
class AuthRegister(Resource):
    """ User registration route
    User register's then receives the user's information
    and access token
    """

    @api.doc("Authentication register route")
    @api.expect(auth_register, validate=True)
    def post(self):
        """ Register to app """
        # Grab the register data
        register_data = request.get_json()
        return AuthService.register(register_data)
