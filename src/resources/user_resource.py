from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import UserService, ExternalService
from src.dto import UserDto

from src.schemas import UpdateUserDataSchema
from src.utils import validation_error


api = UserDto.api
data_resp = UserDto.data_resp
search_data_resp = UserDto.search_data_resp
update_schema = UpdateUserDataSchema()


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

    @api.doc(
        "Delete a specific user account",
        responses={
            200: ("User account successfully deleted", data_resp),
            401: ("Authentication required"),
            403: ("Unable to delete an account which is not your's"),
            404: "User not found!",
        },
    )
    @jwt_required
    def delete(self, uuid):
        """ Delete a specific user's account by their uuid """
        user_uuid = get_jwt_identity()
        return UserService.delete_account(uuid, user_uuid)

    user_data = UserDto.user_data

    @api.doc(
        "Update a specific username",
        responses={
            200: ("Username successfully updated", data_resp),
            401: ("Authentication required"),
            403: ("Unable to update an account which is not your's"),
            404: "User not found!",
        },
    )
    @jwt_required
    @api.expect(user_data, validate=True)
    def patch(self, uuid):
        user_uuid = get_jwt_identity()
        data = request.get_json()
        # Validate data
        if (errors := update_schema.validate(data)):
            return validation_error(False, errors)
        return UserService.update_user_data(uuid, user_uuid, data)


@api.route("/preferences_defined")
class UserResource(Resource):
    @api.doc(
        "Set preferences defined to true",
        responses={
            201: ("User data successfully sent"),
            401: ("Authentication required"),
            403: ("Unable to update an account which is not your's"),
            404: "User not found!",
        },
    )
    @jwt_required
    def put(self):
        """ Set preferences defined to true """
        user_uuid = get_jwt_identity()

        return UserService.set_preferences_defined(user_uuid)


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
            401: ("Authentication required"),
            404: "User or Genre not found!",
        }
    )
    @jwt_required
    def delete(self, genre_id):
        """ Unlike a genre (connected user) """
        user_uuid = get_jwt_identity()

        return UserService.unlike_genre(genre_id, user_uuid)
