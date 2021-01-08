from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import TrackService
from src.dto import TrackDto, UserDto

api = TrackDto.api
data_resp = TrackDto.data_resp
genres_resp = UserDto.genres_resp
meta_resp = UserDto.meta_resp
history_resp = TrackDto.history_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackResource(Resource):
    @api.doc(
        "Get list of recommended Tracks",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of recommended Tracks """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return TrackService.get_recommended_tracks(page, user_uuid)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackSearchResource(Resource):
    @api.doc(
        "Search tracks",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of track's data by term """
        user_uuid = get_jwt_identity()
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return TrackService.search_track_data(search_term, page, user_uuid)


@api.route("/genres")
class TrackGenresResource(Resource):
    @api.doc(
        "Get track genres",
        responses={
            200: ("Track data successfully sent", genres_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get track genres """
        user_uuid = get_jwt_identity()
        return TrackService.get_ordered_genre(user_uuid)


@api.route("/<int:track_id>/meta")
class TrackMetaResource(Resource):
    @api.doc(
        "Get track-user (connected user) meta",
        responses={
            200: ("Track-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, track_id):
        """ Get track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return TrackService.get_meta(user_uuid, track_id)

    content_meta = UserDto.content_meta

    @api.doc(
        "Update track-user (connected user) meta",
        responses={
            201: ("Track-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Track not found!",
        },
    )
    @jwt_required
    @api.expect(content_meta, validate=True)
    def patch(self, track_id):
        """ Update track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return TrackService.update_meta(user_uuid, track_id, data)


@api.route("/history", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackHistoryResource(Resource):
    @api.doc(
        "Get the history of listened track",
        responses={
            200: ("History of listened track data successfully sent", history_resp),
            401: ("Authentication required"),
            404: "User not found!",
        },
    )
    @jwt_required
    def get(self):
        """ Get the history of listened """
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1

        return TrackService.get_history(user_uuid, page)


@api.route("/<int:track_id>/bad_recommendation")
class TrackBadRecommendation(Resource):
    bad_recommendation = UserDto.bad_recommendation

    @api.doc(
        "Add Track-user (connected user) bad recommendation",
        responses={
            200: ("Track-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, track_id):
        """ Add Track-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return TrackService.add_bad_recommendation(user_uuid, track_id, data)
