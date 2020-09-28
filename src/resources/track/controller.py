from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import TrackService
from .dto import TrackDto

api = TrackDto.api
data_resp = TrackDto.data_resp


@api.route("/<string:track_id>")
class TrackController(Resource):
    @api.doc(
        "Get a specific track",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
            404: "Track not found!",
        },
    )
    @jwt_required
    def get(self, track_id):
        """ Get a specific track's data by their id """
        return TrackService.get_track_data(track_id)
