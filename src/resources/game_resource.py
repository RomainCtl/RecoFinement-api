from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import GameService
from src.dto import GameDto

api = GameDto.api
data_resp = GameDto.data_resp
genres_resp = GameDto.genres_resp
meta_resp = GameDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameResource(Resource):
    @api.doc(
        "Get list of recommended Games",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of recommended Games """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return GameService.get_recommended_games(page, user_uuid)


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
        except (ValueError, TypeError):
            page = 1
        return GameService.search_game_data(search_term, page)


@api.route("/genres")
class GameGenresResource(Resource):
    @api.doc(
        "Get game genres",
        responses={
            200: ("Game genres data successfully sent", genres_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get game genres """
        return GameService.get_ordered_genre()


@api.route("/<int:game_id>/meta")
class GameMetaResource(Resource):
    @api.doc(
        "Get game-user (connected user) meta",
        responses={
            200: ("Game-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, game_id):
        """ Get track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return GameService.get_meta(user_uuid, game_id)

    game_meta = GameDto.game_meta

    @api.doc(
        "Update game-user (connected user) meta",
        responses={
            201: ("Game-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Game not found!",
        },
    )
    @jwt_required
    @api.expect(game_meta, validate=True)
    def patch(self, game_id):
        """ Update game-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return GameService.update_meta(user_uuid, game_id, data)
