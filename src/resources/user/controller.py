from flask_restx import Resource

from .service import UserService
from .dto import UserDto

api = UserDto.api
data_resp = UserDto.data_resp


@api.route("/<string:uuid>")
class UserGet(Resource):
    @api.doc(
        "Get a specific user",
        responses={
            200: ("User data successfully sent", data_resp),
            404: "User not found!",
        },
    )
    def get(self, uuid):
        """ Get a specific user's data by their uuid """
        return UserService.get_track_data(uuid)
