from flask_restx import Namespace, fields

from .base import UserBaseObj, messageObj


class UserDto:
    api = Namespace("user", description="User related operations.")
    user = api.model(
        "User object",
        UserBaseObj,
    )

    data_resp = api.model(
        "User Data Response",
        {
            **messageObj,
            "user": fields.Nested(user),
        },
    )
