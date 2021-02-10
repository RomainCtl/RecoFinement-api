from src.dto.application_dto import ApplicationDto
from flask import request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import MovieService, ContentService
from src.dto import MovieDto, UserDto

api = MovieDto.api
data_resp = MovieDto.data_resp
genres_resp = UserDto.genres_resp
meta_resp = UserDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class MovieResource(Resource):
    @api.doc(
        "Get list of the most popular Movies",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Movies """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return MovieService.get_popular_movies(page, user_uuid)

    movie_additional = MovieDto.movie_additional_base

    @api.doc(
        "Add additional Movie for validation",
        responses={
            200: ("Additional movie added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(movie_additional, validate=True)
    def post(self):
        """ Add additional Movie for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return MovieService.add_additional_movie(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class MovieUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Movies for the connected user",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Movies for the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return MovieService.get_recommended_movies_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class MovieGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Movies for the groups of the connected user",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Movies for the groups of the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return MovieService.get_recommended_movies_for_group(args["page"], user_uuid, args["reco_engine"])


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class MovieSearchResource(Resource):
    @api.doc(
        "Search movies",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of movie's data by term """
        user_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return MovieService.search_movie_data(search_term, page, user_uuid)


@api.route("/genres")
class MovieGenresResource(Resource):
    @api.doc(
        "Get movie genres",
        responses={
            200: ("Movie genres data successfully sent", genres_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get movie genres """
        user_uuid = get_jwt_identity()
        return MovieService.get_ordered_genre(user_uuid)


@api.route("/<int:content_id>/meta")
class MovieMetaResource(Resource):
    @api.doc(
        "Get movie-user (connected user) meta",
        responses={
            200: ("Movie-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get movie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update movie-user (connected user) meta",
        responses={
            201: ("Movie-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Movie not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, content_id):
        """ Update movie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


@api.route("/<int:content_id>/bad_recommendation")
class MovieBadRecommendation(Resource):
    bad_recommendation = ApplicationDto.application_bad_recommendation

    @api.doc(
        "Add Movie-user (connected user) bad recommendation",
        responses={
            200: ("Movie-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, content_id):
        """ Add Movie-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return MovieService.add_bad_recommendation(user_uuid, content_id, data)


@api.route("/additional", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class MovieAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Movies (by user)",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Movies (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return MovieService.get_additional_movie(user_uuid, args["page"])


@api.route("/additional/<int:movie_id>")
class MovieAdditionalValidationResource(Resource):
    @api.doc(
        "Validate (put) added Movies (by user)",
        responses={
            201: ("Additional movie data successfully validated"),
            401: ("Authentication required"),
            404: ("User or movie not found!"),
        },
    )
    @jwt_required
    def put(self, movie_id):
        """ Validate (put) added Movies (by user) """
        user_uuid = get_jwt_identity()

        return MovieService.validate_additional_movie(user_uuid, movie_id)

    @api.doc(
        "Decline (delete) added Movies (by user)",
        responses={
            201: ("Additional movie successfully deleted"),
            401: ("Authentication required"),
            404: ("User or movie not found!"),
        },
    )
    @jwt_required
    def delete(self, movie_id):
        """ Decline (delete) added Movies (by user) """
        user_uuid = get_jwt_identity()

        return MovieService.decline_additional_movie(user_uuid, movie_id)