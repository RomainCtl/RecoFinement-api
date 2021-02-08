from flask_restx import Namespace, fields

from .base import ProfileBaseObj, GroupBaseObj, ProfileItemObj, messageObj, paginationObj, GenreBaseObj, MetaProfileContentBaseObj, MetaProfileApplicationItemObj, MetaProfileBookItemObj, MetaProfileGameItemObj, MetaProfileMovieItemObj, MetaProfileSerieItemObj, MetaProfileTrackItemObj, GenreBase2Obj, ResultApplicationItemObj, ResultBookItemObj, ResultGameItemObj, ResultMovieItemObj, ResultSerieItemObj, ResultTrackItemObj


class ProfileDto:
    api = Namespace("profile", description="Profile related operations.")

    # Objects
    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    api.models[MetaProfileContentBaseObj.name] = MetaProfileContentBaseObj
    meta_profile_content_base = MetaProfileContentBaseObj

    api.models[MetaProfileApplicationItemObj.name] = MetaProfileApplicationItemObj
    meta_profile_application_item = MetaProfileApplicationItemObj

    api.models[MetaProfileBookItemObj.name] = MetaProfileBookItemObj
    meta_profile_book_item = MetaProfileBookItemObj

    api.models[MetaProfileGameItemObj.name] = MetaProfileGameItemObj
    meta_profile_game_item = MetaProfileGameItemObj

    api.models[MetaProfileMovieItemObj.name] = MetaProfileMovieItemObj
    meta_profile_movie_item = MetaProfileMovieItemObj

    api.models[MetaProfileSerieItemObj.name] = MetaProfileSerieItemObj
    meta_profile_serie_item = MetaProfileSerieItemObj

    api.models[MetaProfileTrackItemObj.name] = MetaProfileTrackItemObj
    meta_profile_track_item = MetaProfileTrackItemObj

    api.models[ProfileBaseObj.name] = ProfileBaseObj
    profile_base = ProfileBaseObj

    api.models[ProfileItemObj.name] = ProfileItemObj
    profile_item = ProfileItemObj

    api.models[GenreBase2Obj.name] = GenreBase2Obj
    liked_genres2_base = GenreBase2Obj

    api.models[ResultApplicationItemObj.name] = ResultApplicationItemObj
    result_app_item = ResultApplicationItemObj

    api.models[ResultBookItemObj.name] = ResultBookItemObj
    result_book_item = ResultBookItemObj

    api.models[ResultGameItemObj.name] = ResultGameItemObj
    result_game_item = ResultGameItemObj

    api.models[ResultMovieItemObj.name] = ResultMovieItemObj
    result_movie_item = ResultMovieItemObj

    api.models[ResultSerieItemObj.name] = ResultSerieItemObj
    result_serie_item = ResultSerieItemObj

    api.models[ResultTrackItemObj.name] = ResultTrackItemObj
    result_track_item = ResultTrackItemObj

    # Responses
    data_resp = api.clone(
        "Profile Data Response",
        messageObj,
        {
            "profile": fields.Nested(profile_item)
        }
    )

    data_resp_list = api.clone(
        "Profile List Data Response",
        messageObj,
        {
            "profile": fields.List(fields.Nested(profile_item))
        }
    )

    liked_genres_resp_list = api.clone(
        "Profile liked genres list",
        messageObj,
        {
            "profile": fields.List(fields.Nested(liked_genres2_base))
        }
    )

    search_data_resp = api.clone(
        "Profile Research Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(profile_base))
        }
    )
    genres_resp = api.clone(
        "Content genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    meta_application_resp = api.clone(
        "MetaProfileapplication Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_application_item))
        }
    )

    meta_book_resp = api.clone(
        "MetaProfilebook Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_book_item))
        }
    )

    meta_game_resp = api.clone(
        "MetaProfilegame Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_game_item))
        }
    )

    meta_movie_resp = api.clone(
        "MetaProfilemovie Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_movie_item))
        }
    )

    meta_serie_resp = api.clone(
        "MetaProfileserie Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_serie_item))
        }
    )

    meta_track_resp = api.clone(
        "MetaProfiletrack Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(meta_profile_track_item))
        }
    )

    result_app_resp = api.clone(
        "Result app_ Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_app_item))
        }
    )
    result_book_resp = api.clone(
        "Result book Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_book_item))
        }
    )
    result_game_resp = api.clone(
        "Result game Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_game_item))
        }
    )
    result_movie_resp = api.clone(
        "Result movi Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_movie_item))
        }
    )
    result_serie_resp = api.clone(
        "Result seri Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_serie_item))
        }
    )
    result_track_resp = api.clone(
        "Result trac Data resp",
        messageObj,
        {
            "content": fields.List(fields.Nested(result_track_item))
        }
    )

    # Expected data
    profile_data = api.model(
        "ProfileDataExpected",
        {
            "profilename": fields.String(min=4, max=15)
        },
    )

    bad_recommendation = api.model(
        "ApplicationMetaExpected",
        {
            "reason_categorie": fields.List(fields.String),
            "reason": fields.List(fields.String)
        }
    )

    content_meta = api.model(
        "ContentProfileMetaExpected",
        {
            "rating": fields.Integer(min=0, max=5, required=True),
            "last_rating_date": fields.DateTime(required=True),
            "review_see_count": fields.Integer(min=0, required=True),
            "last_review_see_date": fields.DateTime(required=True),
            "count": fields.Integer(min=0, required=True),
            "last_count_increment": fields.DateTime(required=True),
        }
    )
