from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import ApplicationService
from src.dto import ApplicationDto

api = ApplicationDto.api
data_resp = ApplicationDto.data_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ApplicationResource(Resource):
    @api.doc(
        "Get list of the most popular Applications",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Applications """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return ApplicationService.get_most_popular_applications(page)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ApplicationSearchResource(Resource):
    @api.doc(
        "Search applications",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of application's data by term """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return ApplicationService.search_application_data(search_term, page)
