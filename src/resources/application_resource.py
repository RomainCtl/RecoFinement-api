from flask import request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import ApplicationService, ContentService
from src.dto import ApplicationDto, UserDto

api = ApplicationDto.api
data_resp = ApplicationDto.data_resp
genres_resp = UserDto.genres_resp
meta_resp = UserDto.meta_resp


@api.route("")
class ApplicationResource(Resource):
    @api.doc(
        "Get list of the most popular Applications",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
        params={"page": {"in": "query", "type": "int", "default": 1}}
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Applications """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return ApplicationService.get_popular_applications(page, user_uuid)

    application_additional = ApplicationDto.application_additional_base

    @api.doc(
        "Add additional Application for validation",
        responses={
            200: ("Additional application added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(application_additional, validate=True)
    def post(self):
        """ Add additional Application for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ApplicationService.add_additional_application(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class ApplicationUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Applications for the connected user",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Applications for the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return ApplicationService.get_recommended_applications_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class ApplicationGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Applications for the groups of the connected user",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Applications for the groups of the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return ApplicationService.get_recommended_applications_for_group(args["page"], user_uuid, args["reco_engine"])


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


@api.route("/<int:content_id>/meta")
class ApplicationMetaResource(Resource):
    @api.doc(
        "Get application-user (connected user) meta",
        responses={
            200: ("Application-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get application-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update application-user (connected user) meta",
        responses={
            201: ("Application-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Application not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, content_id):
        """ Update application-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


@api.route("/<int:content_id>/bad_recommendation")
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
    def post(self, content_id):
        """ Add application-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ApplicationService.add_bad_recommendation(user_uuid, content_id, data)


@api.route("/additional", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ApplicationAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Applications (by user)",
        responses={
            200: ("Application data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Applications (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return ApplicationService.get_additional_application(user_uuid, args["page"])


@api.route("/additional/<int:app_id>")
class ApplicationAdditionalValidationResource(Resource):
    @api.doc(
        "Validate (put) added Applications (by user)",
        responses={
            201: ("Additional application data successfully validated"),
            401: ("Authentication required"),
            403: ("Permission missing"),
            404: ("User or application not found!"),
        },
    )
    @jwt_required
    def put(self, app_id):
        """ Validate (put) added Applications (by user) """
        user_uuid = get_jwt_identity()

        return ApplicationService.validate_additional_application(user_uuid, app_id)

    @api.doc(
        "Decline (delete) added Applications (by user)",
        responses={
            201: ("Additional application successfully deleted"),
            401: ("Authentication required"),
            403: ("Permission missing"),
            404: ("User or application not found!"),
        },
    )
    @jwt_required
    def delete(self, app_id):
        """ Decline (delete) added Applications (by user) """
        user_uuid = get_jwt_identity()

        return ApplicationService.decline_additional_application(user_uuid, app_id)
