from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import TrackService
from src.dto import TrackDto

api = TrackDto.api
data_resp = TrackDto.data_resp
genres_resp = TrackDto.genres_resp
meta_resp = TrackDto.meta_resp
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
        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return TrackService.search_track_data(search_term, page)


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
        return TrackService.get_ordered_genre()


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

    track_meta = TrackDto.track_meta

    @api.doc(
        "Update track-user (connected user) meta",
        responses={
            201: ("Track-User meta data successfully sent"),
            401: ("Authentication required"),
            404: "User or Track not found!",
        },
    )
    @jwt_required
    @api.expect(track_meta, validate=True)
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
