from flask import request,current_app
from flask_restx import Resource
from flask_jwt_extended import get_raw_jwt, jwt_required
import asyncio
from threading import Thread

from src.utils import validation_error

# Auth modules
from src.service import AuthService, ExternalService
from src.dto import AuthDto
from src.schemas import LoginSchema, RegisterSchema, ResetSchema, ForgetSchema

api = AuthDto.api
auth_success = AuthDto.auth_success

login_schema = LoginSchema()
register_schema = RegisterSchema()
reset_schema = ResetSchema()
forget_schema = ForgetSchema()


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

        res,code = AuthService.login(login_data)
        #current_app.logger.info('before get spotify data')
        thread = Thread(target=ExternalService.get_spotify_data, args=(res['user']['uuid'],current_app._get_current_object()))
        thread.daemon = True
        thread.start()
        
        return res,code 


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
            204: (""),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def post(self):
        """ User logout """
        token = get_raw_jwt()

        return AuthService.logout(token)

@api.route("/forget")
class AuthForgotPassword(Resource):
    auth_forgot=AuthDto.auth_forgot
    """ User password forgot """
    @api.doc(
        "Auth password forgot",
        responses={
            204: ("Successfully reset mail sent."),
        },
    )
    @api.doc(security=None)
    @api.expect(auth_forgot, validate=True)
    def post(self):
        """ User password forgot """
        data=request.get_json()
        # Validate data
        if (errors := forget_schema.validate(data)):
            return validation_error(False, errors)
        return AuthService.forget(data['email'])

@api.route("/reset")
class AuthResetPassword(Resource):
    auth_reset=AuthDto.auth_reset
    """ User password reset """
    @api.doc(
        "Auth password reset",
        responses={
            204: ("Successfully reset password"),
        },
    )
    @api.doc(security=None)
    @api.expect(auth_reset, validate=True)
    def post(self):
        """ User password reset"""
        data = request.get_json()
        # Validate data
        if (errors := reset_schema.validate(data)):
            return validation_error(False, errors)
        return AuthService.reset(data)
        
