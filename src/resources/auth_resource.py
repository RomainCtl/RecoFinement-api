from flask import request
from flask_restx import Resource
from flask_jwt_extended import get_raw_jwt, jwt_required

from src.utils import validation_error

# Auth modules
from src.service import AuthService
from src.dto import AuthDto
from src.schemas import LoginSchema, RegisterSchema

api = AuthDto.api
auth_success = AuthDto.auth_success

login_schema = LoginSchema()
register_schema = RegisterSchema()


@api.route("/login")
class AuthLogin(Resource):
    """ User login endpoint
    User registers then receives the user's information and access_token
    """

    auth_login = AuthDto.auth_login

    @api.doc(
        "Auth login",
        responses={
            200: ("Logged in", auth_success),
            401: "Failed to log in.",
        },
    )
    @api.doc(security=None)
    @api.expect(auth_login, validate=True)
    def post(self):
        """ Login using email and password """
        # Grab the json data
        login_data = request.get_json()

        # Validate data
        if (errors := login_schema.validate(login_data)):
            return validation_error(False, errors)

        return AuthService.login(login_data)


@api.route("/register")
class AuthRegister(Resource):
    """ User register endpoint
    User registers then receives the user's information and access_token
    """

    auth_register = AuthDto.auth_register

    @api.doc(
        "Auth registration",
        responses={
            201: ("Successfully registered user.", auth_success),
            400: "Malformed data or validations failed.",
        },
    )
    @api.doc(security=None)
    @api.expect(auth_register, validate=True)
    def post(self):
        """ User registration """
        # Grab the json data
        register_data = request.get_json()

        # Validate data
        if (errors := register_schema.validate(register_data)):
            return validation_error(False, errors)

        return AuthService.register(register_data)


@api.route("/logout")
class AuthLogout(Resource):
    """ User logout endpoint
    """
    @api.doc(
        "Auth logout",
        responses={
            204: ("Successfully logout user."),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def post(self):
        """ User logout """
        token = get_raw_jwt()

        return AuthService.logout(token)
