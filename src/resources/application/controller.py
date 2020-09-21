from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import ApplicationService
from .dto import ApplicationDto

api = ApplicationDto.api
data_resp = ApplicationDto.data_resp


@api.route("/<string:uid>")
class ApplicationGet(Resource):
    @api.doc(
        "Get a specific application",
        responses={
            200: ("Application data successfully sent", data_resp),
            404: "Application not found!",
        },
    )
    @jwt_required
    def get(self, gid):
        """ Get a specific application's data by their gid """
        return ApplicationService.get_application_data(gid)
