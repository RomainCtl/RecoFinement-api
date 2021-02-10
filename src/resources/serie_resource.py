from flask import request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import SerieService, ContentService
from src.dto import SerieDto, UserDto

api = SerieDto.api
data_resp = SerieDto.data_resp
genres_resp = UserDto.genres_resp
episodes_resp = SerieDto.episodes_resp
meta_resp = UserDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieResource(Resource):
    @api.doc(
        "Get list of the most popular Series",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Series """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return SerieService.get_popular_series(page, user_uuid)

    serie_additional = SerieDto.serie_additional_base

    @api.doc(
        "Add additional Serie for validation",
        responses={
            200: ("Additional serie added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(serie_additional, validate=True)
    def post(self):
        """ Add additional Serie for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return SerieService.add_additional_serie(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class SerieUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Series for the connected user",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Series for the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return SerieService.get_recommended_series_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class SerieGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Series for the groups of the connected user",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Series for the groups of the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return SerieService.get_recommended_series_for_group(args["page"], user_uuid, args["reco_engine"])


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieSearchResource(Resource):
    @api.doc(
        "Search series",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of serie's data by term """
        user_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return SerieService.search_serie_data(search_term, page, user_uuid)


@api.route("/genres")
class SerieGenreResource(Resource):
    @api.doc(
        "Get serie genres",
        responses={
            200: ("Serie data successfully sent", genres_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self):
        """ Get serie genres """
        user_uuid = get_jwt_identity()
        return SerieService.get_ordered_genre(user_uuid)


@api.route("/<int:content_id>/episodes")
class SerieEpisodeResource(Resource):
    @api.doc(
        "Get series episodes",
        responses={
            200: ("Series episodes data sent", episodes_resp),
            404: "Series not found!",
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get series episodes """
        return SerieService.get_episodes(content_id)


@api.route("/<int:content_id>/meta")
class SerieMetaResource(Resource):
    @api.doc(
        "Get serie-user (connected user) meta",
        responses={
            200: ("Serie-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get serie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update serie-user (connected user) meta",
        responses={
            201: ("Serie-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Serie not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, content_id):
        """ Update serie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


@api.route("/<int:content_id>/bad_recommendation")
class SerieBadRecommendation(Resource):
    bad_recommendation = SerieDto.serie_bad_recommendation

    @api.doc(
        "Add Serie-user (connected user) bad recommendation",
        responses={
            200: ("Serie-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, content_id):
        """ Add Serie-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return SerieService.add_bad_recommendation(user_uuid, content_id, data)

@api.route("/additional", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Series (by user)",
        responses={
            200: ("Series data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Series (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return SerieService.get_additional_serie(user_uuid, args["page"])


@api.route("/additional/<int:serie_id>")
class SerieAdditionalResource(Resource):
    @api.doc(
        "Validate (put) added Series (by user)",
        responses={
            201: ("Additional series data successfully validated"),
            401: ("Authentication required"),
            404: ("User or series not found!"),
        },
    )
    @jwt_required
    def put(self, serie_id):
        """ Validate (put) added Series (by user) """
        user_uuid = get_jwt_identity()

        return SerieService.validate_additional_serie(user_uuid, serie_id)

    @api.doc(
        "Decline (delete) added Series (by user)",
        responses={
            201: ("Additional series successfully deleted"),
            401: ("Authentication required"),
            404: ("User or series not found!"),
        },
    )
    @jwt_required
    def delete(self, serie_id):
        """ Decline (delete) added Series (by user) """
        user_uuid = get_jwt_identity()

        return SerieService.decline_additional_serie(user_uuid, serie_id)