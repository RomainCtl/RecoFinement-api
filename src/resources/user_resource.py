from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import UserService
from src.dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp
search_data_resp = UserDto.search_data_resp


@api.route("/<string:uuid>")
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

@api.route("/username")
class UserResource(Resource):
    @api.doc(
        "Update a specific username",
        responses={
            200: ("Username successfully updated", data_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def patch(self):
        """ Update a specific username's data by their uuid """
        user_uuid = get_jwt_identity()
        data=request.get_json()
        return UserService.update_username(user_uuid,data['username'])
    
@api.route("/password")
class UserResource(Resource):
    @api.doc(
        "Update a specific user password",
        responses={
            200: ("User password successfully updated", data_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def patch(self):
        """ Update a specific user's password by their uuid """
        user_uuid = get_jwt_identity()
        data=request.get_json()
        return UserService.update_password(user_uuid,data['password'])

@api.route("/delete")
class UserResource(Resource):
    @api.doc(
        "Delete a specific user account",
        responses={
            200: ("User account successfully deleted", data_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def delete(self):
        """ Delete a specific user's account by their uuid """
        user_uuid = get_jwt_identity()
        return UserService.delete_account(user_uuid)

@api.route("/password/forgot")
class UserResource(Resource):
    @api.doc(
        "Send a specific token by email to reset user password",
        responses={
            200: ("Email successfully sent", data_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def post(self):
        """ Delete a specific user's account by their uuid """
        data=request.get_json()
        return UserService.forgot_password(data['email'])

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
        except (ValueError,TypeError):
            page = 1
        return UserService.search_user_data(search_term, page)


@api.route("/application")
class UserApplicationResource(Resource):

    app_rating = UserDto.app_rating

    @api.doc(
        "Give rate to an application",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Application not found!",
        }
    )
    @jwt_required
    @api.expect(app_rating, validate=True)
    def post(self):
        """ Give rate to an application """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_application(rate_data["app_id"], rate_data["rating"], user_uuid)


@api.route("/book")
class UserBookResource(Resource):

    book_rating = UserDto.book_rating

    @api.doc(
        "Give rate to a book",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Book not found!",
        }
    )
    @jwt_required
    @api.expect(book_rating, validate=True)
    def post(self):
        """ Give rate to a book """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_book(rate_data["isbn"], rate_data["rating"], user_uuid)


@api.route("/game")
class UserGameResource(Resource):

    game_rating = UserDto.game_rating

    @api.doc(
        "Give rate to a game",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Game not found!",
        }
    )
    @jwt_required
    @api.expect(game_rating, validate=True)
    def post(self):
        """ Give rate to a game """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_game(rate_data["game_id"], rate_data["rating"], user_uuid)


@api.route("/movie")
class UserMovieResource(Resource):

    movie_rating = UserDto.movie_rating

    @api.doc(
        "Give rate to a movie",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Movie not found!",
        }
    )
    @jwt_required
    @api.expect(movie_rating, validate=True)
    def post(self):
        """ Give rate to a movie """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_movie(rate_data["movie_id"], rate_data["rating"], user_uuid)


@api.route("/serie")
class UserSerieResource(Resource):

    serie_rating = UserDto.serie_rating

    @api.doc(
        "Give rate to a serie",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Serie not found!",
        }
    )
    @jwt_required
    @api.expect(serie_rating, validate=True)
    def post(self):
        """ Give rate to a serie """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_serie(rate_data["serie_id"], rate_data["rating"], user_uuid)


@api.route("/track")
class UserTrackResource(Resource):

    track_rating = UserDto.track_rating

    @api.doc(
        "Give rate to a track",
        responses={
            200: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Track not found!",
        }
    )
    @jwt_required
    @api.expect(track_rating, validate=True)
    def post(self):
        """ Give rate to a track """
        user_uuid = get_jwt_identity()

        # Grab the json data
        rate_data = request.get_json()

        return UserService.rate_track(rate_data["track_id"], rate_data["rating"], user_uuid)


@api.route("/genre")
class UserGenreResource(Resource):

    like_genre = UserDto.like_genre

    @api.doc(
        "Like a genre",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Genre not found!",
        }
    )
    @jwt_required
    @api.expect(like_genre, validate=True)
    def post(self):
        """ Like a genre """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return UserService.like_genre(data["genre_id"], user_uuid)

    @api.doc(
        "Unlike a genre",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Genre not found!",
        }
    )
    @jwt_required
    @api.expect(like_genre, validate=True)
    def delete(self):
        """ Unlike a genre """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return UserService.unlike_genre(data["genre_id"], user_uuid)

    @api.doc(
        "Liked genres",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User not found!",
        }
    )
    @jwt_required
    @api.expect(like_genre, validate=True)
    def get(self):
        """ Liked genres """
        user_uuid = get_jwt_identity()

        return UserService.liked_genres(user_uuid)