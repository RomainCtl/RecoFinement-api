from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import GameService
from .dto import GameDto

api = GameDto.api
data_resp = GameDto.data_resp


@api.route("/<string:uid>")
class GameController(Resource):
    @api.doc(
        "Get a specific game",
        responses={
            200: ("Game data successfully sent", data_resp),
            404: "Game not found!",
        },
    )
    @jwt_required
    def get(self, uid):
        """ Get a specific game's data by their uid """
        return GameService.get_game_data(uid)
