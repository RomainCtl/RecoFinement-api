from flask_restx import Namespace, fields

from .base import TrackBaseObj, TrackItemObj, paginationObj, TrackGenresBaseObj, GenreBaseObj, messageObj


class TrackDto:
    api = Namespace("track", description="Track related operations.")

    # Objects
    api.models[TrackBaseObj.name] = TrackBaseObj
    track_base = TrackBaseObj

    api.models[TrackItemObj.name] = TrackItemObj
    track_item = TrackItemObj

    api.models[TrackGenresBaseObj.name] = TrackGenresBaseObj
    track_genres_base = TrackGenresBaseObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    # Responses
    data_resp = api.clone(
        "Track list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(track_item)),
        },
    )

    genres_resp = api.clone(
        "Track genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    # Excepted data
    track_meta = api.model(
        "TrackMetaExpected",
        {
            "additional_play_count": fields.Integer(min=1),
            "rating": fields.Integer(min=0, max=5),
        }
    )
