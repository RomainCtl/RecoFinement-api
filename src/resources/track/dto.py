from flask_restx import Namespace, fields


class TrackDto:
    api = Namespace("track", description="Track related operations.")
    track = api.model(
        "Track object",
        {
            "track_id": fields.String,
            "title": fields.String,
            "year": fields.Integer,
            "artist_name": fields.String,
            "release": fields.String,
            "track_mmid": fields.String,
            "recording_mbid": fields.String,
            "language": fields.String,
            "rating": fields.Float,
            "rating_count": fields.Integer,
            "url": fields.String,
            "covert_art_url": fields.String,
        },
    )

    data_resp = api.model(
        "Track Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "track": fields.Nested(track),
        },
    )
