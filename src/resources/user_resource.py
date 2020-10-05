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
        except ValueError:
            page = 1
        return UserService.search_user_data(search_term, page)


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
