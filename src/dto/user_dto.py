from flask_restx import Namespace, fields

from .base import UserBaseObj, GroupBaseObj, UserItemObj, UserExportObj, messageObj, paginationObj, GenreBaseObj, MetaUserApplicationItemObj, MetaUserBookItemObj, MetaUserGameItemObj, MetaUserMovieItemObj, MetaUserSerieItemObj, MetaUserTrackItemObj


class UserDto:
    api = Namespace("user", description="User related operations.")

    # Objects
    api.models[UserBaseObj.name] = UserBaseObj
    user_base = UserBaseObj

    api.models[UserItemObj.name] = UserItemObj
    user_item = UserItemObj

    api.models[UserExportObj.name] = UserExportObj
    user_full_obj = UserExportObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    api.models[MetaUserApplicationItemObj.name] = MetaUserApplicationItemObj
    meta_user_app_item = MetaUserApplicationItemObj

    api.models[MetaUserBookItemObj.name] = MetaUserBookItemObj
    meta_user_book_item = MetaUserBookItemObj

    api.models[MetaUserGameItemObj.name] = MetaUserGameItemObj
    meta_user_game_item = MetaUserGameItemObj

    api.models[MetaUserMovieItemObj.name] = MetaUserMovieItemObj
    meta_user_movie_item = MetaUserMovieItemObj

    api.models[MetaUserSerieItemObj.name] = MetaUserSerieItemObj
    meta_user_serie_item = MetaUserSerieItemObj

    api.models[MetaUserTrackItemObj.name] = MetaUserTrackItemObj
    meta_user_track_item = MetaUserTrackItemObj

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
