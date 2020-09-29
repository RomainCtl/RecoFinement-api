from flask_restx import Namespace, fields

from .base import UserBaseObj, messageObj


class AuthDto:
    api = Namespace("auth", description="Authenticate and receive tokens.")

    user_obj = api.model(
        "User object",
        UserBaseObj
    )

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

    auth_success = api.model(
        "Auth success response",
        {
            **messageObj,
            "user": fields.Nested(user_obj),
        },
    )