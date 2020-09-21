from flask_restx import Namespace, fields

class TrackDto:
    api = Namespace("track", description="Track related operations.")
    track = api.model(
        "Track object",
        {
            "gid": fields.String,
            "name": fields.String,
            "artist_name": fields.String,
            "album_name": fields.String,
            "language": fields.String,
            "date_year": fields.Integer,
            "date_month": fields.Integer,
            "date_day": fields.Integer,
            "rating": fields.Float,
            "rating_count": fields.Integer,
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
