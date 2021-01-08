from flask_restx import Namespace, fields

from .base import UserBaseObj, GroupBaseObj, UserItemObj, UserExportObj, messageObj, paginationObj, GenreBaseObj, MetaUserContentBaseObj


class UserDto:
    api = Namespace("user", description="User related operations.")

    # Objects
    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    api.models[MetaUserContentBaseObj.name] = MetaUserContentBaseObj
    meta_user_content_base = MetaUserContentBaseObj

    api.models[UserBaseObj.name] = UserBaseObj
    user_base = UserBaseObj

    api.models[UserItemObj.name] = UserItemObj
    user_item = UserItemObj

    api.models[UserExportObj.name] = UserExportObj
    user_full_obj = UserExportObj

    # Responses
    data_resp = api.clone(
        "User Data Response",
        messageObj,
        {
            "user": fields.Nested(user_item)
        }
    )

    export_user_resp = api.clone(
        "User Exportation Data Response",
        messageObj,
        {
            "user": fields.Nested(user_full_obj)
        }
    )

    search_data_resp = api.clone(
        "User Research Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(user_base))
        }
    )
    genres_resp = api.clone(
        "Content genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    meta_resp = api.clone(
        "MetaUserContent Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_user_content_base)
        }
    )

    # Expected data
    user_data = api.model(
        "UserDataExpected",
        {
            "username": fields.String(min=4, max=15),
            "password": fields.String(min=8, max=128),
            "email": fields.String(min=5, max=64)
        },
    )

    bad_recommendation = api.model(
        "ApplicationMetaExpected",
        {
            "reason_categorie": fields.List(fields.String),
            "reason": fields.List(fields.String)
        }
    )
