from flask_restx import Namespace, fields

class GameDto:
    api = Namespace("game", description="Game related operations.")
    game = api.model(
        "Game object",
        {
            "uid": fields.String,
            "name": fields.String,
            "icon_url": fields.String,
            "rating": fields.Float,
            "rating_count": fields.Integer,
            "price": fields.Float,
            "in_app_purchases": fields.Float,
            "description": fields.String,
            "developer": fields.String,
            "languages": fields.String,
            "size": fields.Integer,
            "primary_genre": fields.String,
            "genres": fields.String,
            "original_release_date": fields.String,
        },
    )

    data_resp = api.model(
        "Game Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "game": fields.Nested(game),
        },
    )
