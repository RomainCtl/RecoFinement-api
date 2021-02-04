from flask_restx import Namespace, fields

from .base import ProfileBaseObj, GroupBaseObj, ProfileItemObj, messageObj, paginationObj, GenreBaseObj, MetaProfileContentBaseObj, MetaProfileApplicationItemObj, MetaProfileBookItemObj, MetaProfileGameItemObj, MetaProfileMovieItemObj, MetaProfileSerieItemObj, MetaProfileTrackItemObj


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

    # Responses
    data_resp = api.clone(
        "Profile Data Response",
        messageObj,
        {
            "profile": fields.Nested(profile_item)
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

    meta_resp = api.clone(
        "MetaProfileContent Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_content_base)
        }
    )

    meta_application_resp = api.clone(
        "MetaProfileapplication Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_application_item)
        }
    )

    meta_book_resp = api.clone(
        "MetaProfilebook Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_book_item)
        }
    )

    meta_game_resp = api.clone(
        "MetaProfilegame Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_game_item)
        }
    )

    meta_movie_resp = api.clone(
        "MetaProfilemovie Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_movie_item)
        }
    )

    meta_serie_resp = api.clone(
        "MetaProfileserie Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_serie_item)
        }
    )

    meta_track_resp = api.clone(
        "MetaProfiletrack Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_profile_track_item)
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
