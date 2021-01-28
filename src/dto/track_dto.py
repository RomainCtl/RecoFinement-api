from flask_restx import Namespace, fields

from .base import TrackBaseObj, TrackItemObj, paginationObj, messageObj, TrackAdditionalBaseObj


class TrackDto:
    api = Namespace("track", description="Track related operations.")

    # Objects
    api.models[TrackBaseObj.name] = TrackBaseObj
    track_base = TrackBaseObj

    api.models[TrackItemObj.name] = TrackItemObj
    track_item = TrackItemObj

    api.models[TrackAdditionalBaseObj.name] = TrackAdditionalBaseObj
    track_additional_base = TrackAdditionalBaseObj

    track_history = api.model("TrackHistory", {
        "last_played_date": fields.DateTime,
        "track": fields.Nested(track_item)
    })

    # Responses
    data_resp = api.clone(
        "Track list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(track_item)),
        },
    )

    history_resp = api.clone(
        "TrackListenedHistory Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(track_history))
        }
    )

    track_bad_recommendation = api.model(
        "TrackBadRecommendationMetaExpected",
        {
            "year": fields.List(fields.String),
            "artist_name": fields.List(fields.String),
            "release": fields.List(fields.String),
            "genres": fields.List(fields.String)
        }
    )