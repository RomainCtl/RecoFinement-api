from flask_restx import Namespace, fields

from .base import UserBaseObj, messageObj


class AuthDto:
    api = Namespace("auth", description="Authenticate and receive tokens.")

    # Objects
    api.models[UserBaseObj.name] = UserBaseObj
    user_base = UserBaseObj

    # Responses
    auth_success = api.model(
        "Auth success response",
        {
            **messageObj,
            "user": fields.Nested(user_base),
            "access_token": fields.String,
        },
    )

    # Excepted data
    auth_login = api.model(
        "Login data",
        {
            "email": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )

    auth_register = api.model(
        "Registration data",
        {
            "email": fields.String(required=True),
            "username": fields.String(required=True),
            "password": fields.String(required=True),
        },
    )

    auth_forgot = api.model(
        "Forgot password",
        {
            "email": fields.String(required=True)
        },
    )

    auth_reset = api.model(
        "Reset password",
        {
            "reset_password_token": fields.String(required=True),
            "password":fields.String(required=True)
        },
    )