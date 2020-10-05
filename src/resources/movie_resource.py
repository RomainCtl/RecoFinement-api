from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import MovieService
from src.dto import MovieDto

api = MovieDto.api
data_resp = MovieDto.data_resp


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
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return MovieService.get_most_popular_movies(page)


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
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return MovieService.search_movie_data(search_term, page)
