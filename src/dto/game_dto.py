from flask_restx import Namespace, fields

from .base import GameBaseObj, paginationObj, messageObj


class GameDto:
    api = Namespace("game", description="Game related operations.")

    # Objects
    api.models[GameBaseObj.name] = GameBaseObj
    game_base = GameBaseObj

    # Responses
    data_resp = api.clone(
        "Game list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(game_base)),
        },
    )

    # Excepted data
    game_meta = api.model(
        "GameMetaExpected",
        {
            "purchase": fields.Boolean,
            "additional_hours": fields.Float(min=0.0),
            "rating": fields.Integer(min=0, max=5),
        }
    )
