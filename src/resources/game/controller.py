from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import GameService
from .dto import GameDto

api = GameDto.api
data_resp = GameDto.data_resp


@api.route("/<string:game_id>")
class GameController(Resource):
    @api.doc(
        "Get a specific game",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
            404: "Game not found!",
        },
    )
    @jwt_required
    def get(self, game_id):
        """ Get a specific game's data by their id """
        return GameService.get_game_data(game_id)
