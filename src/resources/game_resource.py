from flask import request
from flask_restx import Resource, reqparse
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

    game_additional = GameDto.game_additional_base

    @api.doc(
        "Add additional Game for validation",
        responses={
            200: ("Additional game added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(game_additional, validate=True)
    def post(self):
        """ Add additional Game for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return GameService.add_additional_game(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
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

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return GameService.get_recommended_games_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
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

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return GameService.get_recommended_games_for_group(args["page"], user_uuid, args["reco_engine"])


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
    bad_recommendation = GameDto.game_bad_recommendation

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


@api.route("/additional", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class GameAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Game (by user)",
        responses={
            200: ("Game data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Games (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return GameService.get_additional_game(user_uuid, args["page"])


@api.route("/additional/<int:game_id>")
class GameAdditionalValidationResource(Resource):
    @api.doc(
        "Validate (put) added Games (by user)",
        responses={
            201: ("Additional game data successfully validated"),
            401: ("Authentication required"),
            403: ("Permission missing"),
            404: ("User or game not found!"),
        },
    )
    @jwt_required
    def put(self, game_id):
        """ Validate (put) added Games (by user) """
        user_uuid = get_jwt_identity()

        return GameService.validate_additional_game(user_uuid, game_id)

    @api.doc(
        "Decline (delete) added Games (by user)",
        responses={
            201: ("Additional game successfully deleted"),
            401: ("Authentication required"),
            403: ("Permission missing"),
            404: ("User or game not found!"),
        },
    )
    @jwt_required
    def delete(self, game_id):
        """ Decline (delete) added Games (by user) """
        user_uuid = get_jwt_identity()

        return GameService.decline_additional_game(user_uuid, game_id)