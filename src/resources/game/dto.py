from flask_restx import Namespace, fields


class GameDto:
    api = Namespace("game", description="Game related operations.")
    game = api.model(
        "Game object",
        {
            "game_id": fields.String,
            "steamid": fields.String,
            "name": fields.String,
            "short_description": fields.String,
            "header_image": fields.String,
            "website": fields.String,
            "developers": fields.String,
            "publishers": fields.String,
            "price": fields.String,
            "genres": fields.String,
            "recommendations": fields.String,
            "release_date": fields.String,
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
