from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import ProfileService, ExternalService
from src.dto import ProfileDto

from src.schemas import UpdateProfileDataSchema
from src.utils import validation_error


api = ProfileDto.api
data_resp = ProfileDto.data_resp
search_data_resp = ProfileDto.search_data_resp
update_schema = UpdateProfileDataSchema()


@api.route("/<uuid:uuid>")
class ProfileResource(Resource):
    @api.doc(
        "Get a specific profile",
        responses={
            200: ("Profile data successfully sent", data_resp),
            401: ("Authentication required"),
            404: "Profile not found!",
        },
    )
    @jwt_required
    def get(self, uuid):
        """ Get a specific profile's data by their uuid """
        profile_uuid = get_jwt_identity()
        return ProfileService.get_profile_data(uuid, profile_uuid)

    @api.doc(
        "Delete a specific profile account",
        responses={
            200: ("Profile account successfully deleted", data_resp),
            401: ("Authentication required"),
            403: ("Unable to delete an account which is not your's"),
            404: "Profile not found!",
        },
    )
    @jwt_required
    def delete(self, uuid):
        """ Delete a specific profile's account by their uuid """
        profile_uuid = get_jwt_identity()
        return ProfileService.delete_account(uuid, profile_uuid)

    profile_data = ProfileDto.profile_data

    @api.doc(
        "Update a specific profilename",
        responses={
            200: ("Profilename successfully updated", data_resp),
            401: ("Authentication required"),
            403: ("Unable to update an account which is not your's"),
            404: "Profile not found!",
        },
    )
    @jwt_required
    @api.expect(profile_data, validate=True)
    def patch(self, uuid):
        profile_uuid = get_jwt_identity()
        data = request.get_json()
        # Validate data
        if (errors := update_schema.validate(data)):
            return validation_error(False, errors)
        return ProfileService.update_profile_data(uuid, profile_uuid, data)

@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileSearchResource(Resource):
    @api.doc(
        "Search profiles",
        responses={
            200: ("Profile data successfully sent", search_data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Get list of track's data by term """
        profile_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return ProfileService.search_profile_data(search_term, page, profile_uuid)


@api.route("/genre")
class ProfileGenresResource(Resource):
    @api.doc(
        "Get liked genres (connected profile)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "Profile not found!",
        }
    )
    @jwt_required
    def get(self):
        """ Get liked genres (connected profile) """
        profile_uuid = get_jwt_identity()

        return ProfileService.get_genres(profile_uuid)


@api.route("/genre/<int:genre_id>")
class ProfileGenreResource(Resource):
    @api.doc(
        "Like a genre (connected profile)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "Profile or Genre not found!",
        }
    )
    @jwt_required
    def put(self, genre_id):
        """ Like a genre (connected profile) """
        profile_uuid = get_jwt_identity()

        return ProfileService.like_genre(genre_id, profile_uuid)

    @api.doc(
        "Unlike a genre (connected profile)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "Profile or Genre not found!",
        }
    )
    @jwt_required
    def delete(self, genre_id):
        """ Unlike a genre (connected profile) """
        profile_uuid = get_jwt_identity()

        return ProfileService.unlike_genre(genre_id, profile_uuid)