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
meta_resp = ProfileDto.meta_resp
meta_application_resp = ProfileDto.meta_application_resp
meta_book_resp = ProfileDto.meta_book_resp
meta_game_resp = ProfileDto.meta_game_resp
meta_movie_resp = ProfileDto.meta_movie_resp
meta_serie_resp = ProfileDto.meta_serie_resp
meta_track_resp = ProfileDto.meta_track_resp
update_schema = UpdateProfileDataSchema()


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class UserProfileResource(Resource):
    @api.doc(
        "Get a specific profile",
        responses={
            200: ("Profile data successfully sent", search_data_resp),
            401: ("Authentication required"),
            403: ("Permission missing"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of user's profile """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profiles(user_uuid, page)

    profile_data = ProfileDto.profile_data

    @api.doc(
        "Create a new profile",
        responses={
            200: ("Profile successfully created", data_resp),
            401: ("Malformed data or validations failed."),
            401: ("Authentication required"),
            403: ("Permission missing"),
        },
    )
    @jwt_required
    @api.expect(profile_data, validate=True)
    def post(self):
        """ Get list of user's profile """
        user_uuid = get_jwt_identity()

        data = request.get_json()

        return ProfileService.create_profile(data, user_uuid)


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


@api.route("/<uuid:profile_uuid>/genre")
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
    def get(self, profile_uuid):
        """ Get liked genres (connected profile) """
        uuid = get_jwt_identity()

        return ProfileService.get_genres(uuid, profile_uuid)


@api.route("/<uuid:profile_uuid>/genre/<int:genre_id>")
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
    def put(self, genre_id, profile_uuid):
        """ Like a genre (connected profile) """
        user_uuid = get_jwt_identity()

        return ProfileService.like_genre(genre_id, user_uuid, profile_uuid)

    @api.doc(
        "Unlike a genre (connected profile)",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "Profile or Genre not found!",
        }
    )
    @jwt_required
    def delete(self, genre_id, profile_uuid):
        """ Unlike a genre (connected profile) """
        user_uuid = get_jwt_identity()

        return ProfileService.unlike_genre(genre_id, user_uuid, profile_uuid)


@api.route("/<uuid:profile_uuid>/content/<int:content_id>/meta")
class ProfileMetaContentResource(Resource):
    content_meta = ProfileDto.content_meta

    @api.doc(
        "Update or set meta between porfile and content",
        responses={
            201: ("Successfully send"),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def put(self, profile_uuid, content_id):
        """ Update or set meta between porfile and content """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ProfileService.update_meta(profile_uuid, content_id, user_uuid, data)


@api.route("/<uuid:profile_uuid>/application/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaApplicationResource(Resource):
    @api.doc(
        "Get meta between profile and application",
        responses={
            200: ("Successfully send", meta_application_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and application """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_app(profile_uuid, user_uuid, page)


@api.route("/<uuid:profile_uuid>/book/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaBookResource(Resource):
    @api.doc(
        "Get meta between profile and book",
        responses={
            200: ("Successfully send", meta_book_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and book """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_book(profile_uuid, user_uuid, page)


@api.route("/<uuid:profile_uuid>/game/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaGameResource(Resource):
    @api.doc(
        "Get meta between profile and game",
        responses={
            200: ("Successfully send", meta_game_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and game """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_game(profile_uuid, user_uuid, page)


@api.route("/<uuid:profile_uuid>/movie/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaMovieResource(Resource):
    @api.doc(
        "Get meta between profile and movie",
        responses={
            200: ("Successfully send", meta_movie_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and movie """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_movie(profile_uuid, user_uuid, page)


@api.route("/<uuid:profile_uuid>/serie/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaSerieResource(Resource):
    @api.doc(
        "Get meta between profile and serie",
        responses={
            200: ("Successfully send", meta_serie_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and serie """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_serie(profile_uuid, user_uuid, page)


@api.route("/<uuid:profile_uuid>/track/meta", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class ProfileMetaTrackResource(Resource):
    @api.doc(
        "Get meta between profile and track",
        responses={
            200: ("Successfully send", meta_track_resp),
            401: ("Authentication required"),
            404: "User or Profile not found!",
        }
    )
    @jwt_required
    def get(self, profile_uuid):
        """ Get meta between profile and track """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return ProfileService.get_profile_meta_track(profile_uuid, user_uuid, page)
