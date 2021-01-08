from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import SerieService
from src.dto import SerieDto

api = SerieDto.api
data_resp = SerieDto.data_resp
genres_resp = SerieDto.genres_resp
episodes_resp = SerieDto.episodes_resp
meta_resp = SerieDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieResource(Resource):
    @api.doc(
        "Get list of recommended Series",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of recommended Series """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return SerieService.get_recommended_series(page, user_uuid)


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


@api.route("/<int:serie_id>/episodes")
class SerieEpisodeResource(Resource):
    @api.doc(
        "Get series episodes",
        responses={
            200: ("Series episodes data sent", episodes_resp),
            404: "Series not found!",
        }
    )
    @jwt_required
    def get(self, serie_id):
        """ Get series episodes """
        return SerieService.get_episodes(serie_id)


@api.route("/<int:serie_id>/meta")
class SerieMetaResource(Resource):
    @api.doc(
        "Get serie-user (connected user) meta",
        responses={
            200: ("Serie-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, serie_id):
        """ Get serie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return SerieService.get_meta(user_uuid, serie_id)

    serie_meta = SerieDto.serie_meta

    @api.doc(
        "Update serie-user (connected user) meta",
        responses={
            201: ("Serie-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Serie not found!",
        },
    )
    @jwt_required
    @api.expect(serie_meta, validate=True)
    def patch(self, serie_id):
        """ Update serie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return SerieService.update_meta(user_uuid, serie_id, data)


@api.route("/<int:serie_id>/bad_recommendation")
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
    def post(self, serie_id):
        """ Add Serie-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return SerieService.add_bad_recommendation(user_uuid, serie_id, data)