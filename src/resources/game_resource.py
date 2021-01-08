from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import GameService, ContentService
from src.dto import GameDto, UserDto

api = GameDto.api
data_resp = GameDto.data_resp
genres_resp = UserDto.genres_resp
meta_resp = UserDto.meta_resp


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
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return GameService.get_popular_games(page, user_uuid)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Games for the connected user",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Games for the connected user """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return GameService.get_recommended_games_for_user(page, user_uuid)


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Games for the groups of the connected user",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Games for the groups of the connected user """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return GameService.get_recommended_games_for_group(page, user_uuid)


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
        user_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return GameService.search_game_data(search_term, page, user_uuid)


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
        user_uuid = get_jwt_identity()
        return GameService.get_ordered_genre(user_uuid)


@api.route("/<int:content_id>/meta")
class GameMetaResource(Resource):
    @api.doc(
        "Get game-user (connected user) meta",
        responses={
            200: ("Game-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update game-user (connected user) meta",
        responses={
            201: ("Game-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Game not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, content_id):
        """ Update game-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


@api.route("/<int:content_id>/bad_recommendation")
class GameBadRecommendation(Resource):
    bad_recommendation = UserDto.bad_recommendation

    @api.doc(
        "Add Game-user (connected user) bad recommendation",
        responses={
            200: ("Game-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, content_id):
        """ Add Game-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return GameService.add_bad_recommendation(user_uuid, content_id, data)
