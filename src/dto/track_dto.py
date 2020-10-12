from flask_restx import Namespace, fields

from .base import TrackBaseObj, TrackItemObj, paginationObj, TrackGenresBaseObj


class TrackDto:
    api = Namespace("track", description="Track related operations.")

    # Objects
    api.models[TrackBaseObj.name] = TrackBaseObj
    track_base = TrackBaseObj

    api.models[TrackItemObj.name] = TrackItemObj
    track_item = TrackItemObj

    api.models[TrackGenresBaseObj.name] = TrackGenresBaseObj
    track_genres_base = TrackGenresBaseObj

    # Responses
    data_resp = api.clone(
        "Track list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(track_item)),
        },
    )
