from flask_restx import Namespace, fields

from .base import UserBaseObj, messageObj, paginationObj


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

    search_data_resp = api.model(
        "User Research Data Response",
        {
            **paginationObj,
            "content": fields.List(fields.Nested(user)),
        },
    )
