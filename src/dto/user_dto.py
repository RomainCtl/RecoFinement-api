from flask_restx import Namespace, fields

from .base import UserBaseObj, GroupBaseObj, UserItemObj, messageObj, paginationObj


class UserDto:
    api = Namespace("user", description="User related operations.")

    # Objects
    api.models[UserBaseObj.name] = UserBaseObj
    user_base = UserBaseObj

    api.models[UserItemObj.name] = UserItemObj
    user_item = UserItemObj

    # Responses
    data_resp = api.clone(
        "User Data Response",
        messageObj,
        {
            "user": fields.Nested(user_item)
        }
    )

    search_data_resp = api.clone(
        "User Research Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(user_base))
        }
    )

    # Excepted data
    track_rating = api.model(
        "Rating Track",
        {
            "track_id": fields.Integer(required=True),
            "rating": fields.Integer(min=0, max=5, required=True),
        }
    )
