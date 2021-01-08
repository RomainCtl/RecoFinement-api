from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import ApplicationService
from src.dto import ApplicationDto

api = ApplicationDto.api
data_resp = ApplicationDto.data_resp
genres_resp = ApplicationDto.genres_resp
meta_resp = ApplicationDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ApplicationResource(Resource):
    @api.doc(
        "Get list of the recommended Applications",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Applications """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return ApplicationService.get_recommended_applications(page, user_uuid)


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
        user_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return ApplicationService.search_application_data(search_term, page, user_uuid)


@api.route("/genres")
class ApplicatioGenresResource(Resource):
    @api.doc(
        "Get application genres",
        responses={
            200: ("Application genres data successfully sent", genres_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get application genres """
        uuid = get_jwt_identity()
        return ApplicationService.get_ordered_genres(uuid)


@api.route("/<int:app_id>/meta")
class ApplicationMetaResource(Resource):
    @api.doc(
        "Get application-user (connected user) meta",
        responses={
            200: ("Application-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, app_id):
        """ Get application-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ApplicationService.get_meta(user_uuid, app_id)

    application_meta = ApplicationDto.application_meta

    @api.doc(
        "Update application-user (connected user) meta",
        responses={
            201: ("Application-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Application not found!",
        },
    )
    @jwt_required
    @api.expect(application_meta, validate=True)
    def patch(self, app_id):
        """ Update application-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ApplicationService.update_meta(user_uuid, app_id, data)

@api.route("/<int:app_id>/bad_recommendation")
class ApplicationBadRecommendation(Resource):
    bad_recommendation = ApplicationDto.application_bad_recommendation
    @api.doc(
        "Add application-user (connected user) bad recommendation",
        responses={
            200: ("Application-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )

    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, app_id):
        """ Add application-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ApplicationService.add_bad_recommendation(user_uuid, app_id, data)