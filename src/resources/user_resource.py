from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

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
        """ Getlist of track's data by term """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return UserService.search_user_data(search_term, page)
