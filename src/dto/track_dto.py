from flask_restx import Namespace, fields

from .base import TrackBaseObj, paginationObj


class TrackDto:
    api = Namespace("track", description="Track related operations.")
    track = api.model(
        "Track object",
        TrackBaseObj,
    )

    data_resp = api.model(
        "Track Research Data Response",
        {
            **paginationObj,
            "content": fields.List(fields.Nested(track)),
        },
    )
