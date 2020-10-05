from flask_restx import Namespace, fields

from .base import GameBaseObj, paginationObj


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
