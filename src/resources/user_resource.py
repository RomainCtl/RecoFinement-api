from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import UserService
from src.dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp
search_data_resp = UserDto.search_data_resp


@api.route("/<uuid:uuid>")
class UserResource(Resource):
    @api.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", data_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def get(self, uuid):
        """ Get a specific user's data by their uuid """
        return UserService.get_user_data(uuid)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class UserSearchResource(Resource):
    @api.doc(
        "Search users",
        responses={
            200: ("User data successfully sent", search_data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Get list of track's data by term """
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return UserService.search_user_data(search_term, page)


@api.route("/application")
@api.deprecated
class UserApplicationResource(Resource):
    def post(self):
        """ Give rate to an application """
        return {}


@api.route("/book")
@api.deprecated
class UserBookResource(Resource):
    def post(self):
        """ Give rate to a book """
        return {}


@api.route("/game")
@api.deprecated
class UserGameResource(Resource):
    def post(self):
        """ Give rate to a game """
        return {}


@api.route("/movie")
@api.deprecated
class UserMovieResource(Resource):
    def post(self):
        """ Give rate to a movie """
        return {}


@api.route("/serie")
@api.deprecated
class UserSerieResource(Resource):
    def post(self):
        """ Give rate to a serie """
        return {}


@api.route("/track")
@api.deprecated
class UserTrackResource(Resource):
    def post(self):
        """ Give rate to a track """
        return {}


@api.route("/genre")
class UserGenresResource(Resource):
    @api.doc(
        "Get liked genres (connected user)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User not found!",
        }
    )
    @jwt_required
    def get(self):
        """ Get liked genres (connected user) """
        user_uuid = get_jwt_identity()

        return UserService.get_genres(user_uuid)


@api.route("/genre/<int:genre_id>")
class UserGenreResource(Resource):
    @api.doc(
        "Like a genre (connected user)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Genre not found!",
        }
    )
    @jwt_required
    def put(self, genre_id):
        """ Like a genre (connected user) """
        user_uuid = get_jwt_identity()

        return UserService.like_genre(genre_id, user_uuid)

    @api.doc(
        "Unlike a genre (connected user)",
        responses={
            201: ("Successfully send"),
            400: ("You didn't like this genre"),
            401: ("Authentication required"),
            404: "User or Genre not found!",
        }
    )
    @jwt_required
    def delete(self, genre_id):
        """ Unlike a genre (connected user) """
        user_uuid = get_jwt_identity()

        return UserService.unlike_genre(genre_id, user_uuid)
