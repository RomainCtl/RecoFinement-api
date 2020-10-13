from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import GameService
from src.dto import GameDto

api = GameDto.api
data_resp = GameDto.data_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameResource(Resource):
    @api.doc(
        "Get list of the most popular Games",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Games """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return GameService.get_most_popular_games(page)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameSearchResource(Resource):
    @api.doc(
        "Search games",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of game's data by term """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return GameService.search_game_data(search_term, page)


@api.route("/genres")
class GameGenresResource(Resource):
    @api.doc(
        "Get game genres",
        responses={
            200: ("Game genres data successfully sent"),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get game genres """
        return GameService.get_ordered_genre()
