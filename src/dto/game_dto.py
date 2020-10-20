from flask_restx import Namespace, fields

from .base import GameBaseObj, paginationObj, GenreBaseObj, messageObj


class GameDto:
    api = Namespace("game", description="Game related operations.")

    # Objects
    api.models[GameBaseObj.name] = GameBaseObj
    game_base = GameBaseObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    # Responses
    data_resp = api.clone(
        "Game list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(game_base)),
        },
    )

    genres_resp = api.clone(
        "Game genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    # Excepted data
    game_meta = api.model(
        "GameMetaExpected",
        {
            "purchase": fields.Boolean,
            "hours": fields.Integer(min=0),
            "rating": fields.Integer(min=0, max=5),
        }
    )
