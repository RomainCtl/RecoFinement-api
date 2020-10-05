from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import SerieService
from src.dto import SerieDto

api = SerieDto.api
data_resp = SerieDto.data_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieResource(Resource):
    @api.doc(
        "Get list of the most popular Series",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Series """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return SerieService.get_most_popular_series(page)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class SerieSearchResource(Resource):
    @api.doc(
        "Search series",
        responses={
            200: ("Serie data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of serie's data by term """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return SerieService.search_serie_data(search_term, page)
