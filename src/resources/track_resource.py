from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import TrackService
from src.dto import TrackDto

api = TrackDto.api
data_resp = TrackDto.data_resp
genres_resp = TrackDto.genres_resp
meta_resp = TrackDto.meta_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackResource(Resource):
    @api.doc(
        "Get list of the most popular Tracks",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Tracks """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return TrackService.get_most_popular_tracks(page)


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
        except ValueError:
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
