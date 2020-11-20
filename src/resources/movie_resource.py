from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import MovieService
from src.dto import MovieDto

api = MovieDto.api
data_resp = MovieDto.data_resp
genres_resp = MovieDto.genres_resp
meta_resp = MovieDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class MovieResource(Resource):
    @api.doc(
        "Get list of recommended Movies",
        responses={
            200: ("Movie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of recommended Movies """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return MovieService.get_recommended_movies(page, user_uuid)


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


@api.route("/<int:movie_id>/meta")
class MovieMetaResource(Resource):
    @api.doc(
        "Get movie-user (connected user) meta",
        responses={
            200: ("Movie-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, movie_id):
        """ Get movie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return MovieService.get_meta(user_uuid, movie_id)

    movie_meta = MovieDto.movie_meta

    @api.doc(
        "Update movie-user (connected user) meta",
        responses={
            201: ("Movie-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Movie not found!",
        },
    )
    @jwt_required
    @api.expect(movie_meta, validate=True)
    def patch(self, movie_id):
        """ Update movie-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return MovieService.update_meta(user_uuid, movie_id, data)
