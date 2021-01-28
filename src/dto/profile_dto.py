from flask_restx import Namespace, fields

from .base import ProfileBaseObj, GroupBaseObj, ProfileItemObj, messageObj, paginationObj, GenreBaseObj, MetaProfileContentBaseObj


class ProfileDto:
    api = Namespace("profile", description="Profile related operations.")

    # Objects
    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    api.models[MetaProfileContentBaseObj.name] = MetaProfileContentBaseObj
    meta_profile_content_base = MetaProfileContentBaseObj

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
        "ContentMetaExpected",
        {
            "additional_count": fields.Float(min=0.0),
            "rating": fields.Integer(min=0, max=5),
        }
    )
