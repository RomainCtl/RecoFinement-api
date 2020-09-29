from flask_restx import Namespace, fields

from .base import TrackBaseObj, paginationObj


class TrackDto:
    api = Namespace("track", description="Track related operations.")

    # Objects
    api.models[TrackBaseObj.name] = TrackBaseObj
    track_base = TrackBaseObj

    # Responses
    data_resp = api.clone(
        "Track Research Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(track_base)),
        },
    )
