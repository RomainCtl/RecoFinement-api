from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import UserService
from src.dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp


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
