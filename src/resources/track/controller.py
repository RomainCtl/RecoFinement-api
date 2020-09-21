from flask_restx import Resource

from .service import TrackService
from .dto import TrackDto

api = TrackDto.api
data_resp = TrackDto.data_resp


@api.route("/<uuid:gid>")
class TrackGet(Resource):
    @api.doc(
        "Get a specific track",
        responses={
            200: ("Track data successfully sent", data_resp),
            404: "Track not found!",
        },
    )
    def get(self, gid):
        """ Get a specific track's data by their gid """
        return TrackService.get_track_data(gid)
