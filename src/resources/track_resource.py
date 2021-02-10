from flask import request
from flask_restx import Resource, reqparse
from flask_jwt_extended import jwt_required, get_jwt_identity

from src.service import TrackService, ContentService
from src.dto import TrackDto, UserDto

api = TrackDto.api
data_resp = TrackDto.data_resp
genres_resp = UserDto.genres_resp
meta_resp = UserDto.meta_resp
history_resp = TrackDto.history_resp


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
        user_uuid = get_jwt_identity()

        try:
            page = int(request.args.get('page'))
        except (ValueError, TypeError):
            page = 1
        return TrackService.get_popular_tracks(page, user_uuid)

    track_additional = TrackDto.track_additional_base

    @api.doc(
        "Add additional Track for validation",
        responses={
            200: ("Additional track added for validation", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(track_additional, validate=True)
    def post(self):
        """ Add additional Track for validation"""
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return TrackService.add_additional_track(user_uuid, data)


@api.route("/user", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class TrackUserRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Tracks for the connected user",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Tracks for the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return TrackService.get_recommended_tracks_for_user(args["page"], user_uuid, args["reco_engine"])


@api.route("/groups", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}, "reco_engine": {"in": "query", "type": "str", "default": None}}})
class TrackGroupRecommendationResource(Resource):
    @api.doc(
        "Get list of the recommended Tracks for the groups of the connected user",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the recommended Tracks for the groups of the connected user """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        parser.add_argument('reco_engine', type=str, default=None)
        args = parser.parse_args()

        return TrackService.get_recommended_tracks_for_group(args["page"], user_uuid, args["reco_engine"])


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


@api.route("/<int:content_id>/meta")
class TrackMetaResource(Resource):
    @api.doc(
        "Get track-user (connected user) meta",
        responses={
            200: ("Track-User meta data successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    def get(self, content_id):
        """ Get track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        return ContentService.get_meta(user_uuid, content_id)

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
    def patch(self, content_id):
        """ Update track-user (connected user) meta """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return ContentService.update_meta(user_uuid, content_id, data)


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


@api.route("/<int:content_id>/bad_recommendation")
class TrackBadRecommendation(Resource):
    bad_recommendation = TrackDto.track_bad_recommendation

    @api.doc(
        "Add Track-user (connected user) bad recommendation",
        responses={
            200: ("Track-User bad recommendation successfully sent", meta_resp),
            401: ("Authentication required"),
        }
    )
    @jwt_required
    @api.expect(bad_recommendation, validate=True)
    def post(self, content_id):
        """ Add Track-user (connected user) bad recommendation """
        user_uuid = get_jwt_identity()

        # Grab the json data
        data = request.get_json()

        return TrackService.add_bad_recommendation(user_uuid, content_id, data)



@api.route("/additional", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class TrackAdditionalResource(Resource):
    @api.doc(
        "Get list of the added Tracks (by user)",
        responses={
            200: ("Track data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the added Tracks (by user) """
        user_uuid = get_jwt_identity()

        parser = reqparse.RequestParser()
        parser.add_argument('page', type=int, default=1)
        args = parser.parse_args()

        return TrackService.get_additional_track(user_uuid, args["page"])


@api.route("/additional/<int:track_id>")
class TrackAdditionalResource(Resource):
    @api.doc(
        "Validate (put) added Tracks (by user)",
        responses={
            201: ("Additional track data successfully validated"),
            401: ("Authentication required"),
            404: ("User or track not found!"),
        },
    )
    @jwt_required
    def put(self, track_id):
        """ Validate (put) added Tracks (by user) """
        user_uuid = get_jwt_identity()

        return TrackService.validate_additional_track(user_uuid, track_id)

    @api.doc(
        "Decline (delete) added Tracks (by user)",
        responses={
            201: ("Additional track successfully deleted"),
            401: ("Authentication required"),
            404: ("User or track not found!"),
        },
    )
    @jwt_required
    def delete(self, track_id):
        """ Decline (delete) added Tracks (by user) """
        user_uuid = get_jwt_identity()

        return TrackService.decline_additional_track(user_uuid, track_id)