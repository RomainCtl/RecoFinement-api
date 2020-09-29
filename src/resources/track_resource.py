from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import TrackService
from src.dto import TrackDto

api = TrackDto.api
data_resp = TrackDto.data_resp


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackResource(Resource):
    @api.doc(
        "Get tracks",
        responses={
            200: ("Track data successfully sent", data_resp),
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
        return TrackService.search_track_data(search_term, page)