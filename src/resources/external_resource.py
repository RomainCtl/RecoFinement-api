from flask import request, current_app
from flask_restx import Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, decode_token

import asyncio
from threading import Thread

# External service modules
from src.service import ExternalService
from src.dto import ExternalDto

#from src.schemas import UpdateExternalDataSchema
from src.utils import validation_error

api = ExternalDto.api
oauth_external = ExternalDto.oauth_url

@api.route("/spotify")
class ExternalSpotifyResource(Resource):
    @api.doc(
        "Oauth2 Spotify",
        responses={
            201: ("Successfully send", oauth_external),
            401: ("Authentication required"),
            404: "User not found!",
        }
    )
    @jwt_required
    def get(self):
        """ Get oauth spotify """
        user_uuid = get_jwt_identity()

        return ExternalService.get_spotify_oauth(user_uuid)

@api.route("/spotify/callback")
class ExternalSpotifyCallbackResource(Resource):
    oauth_external = ExternalDto.oauth_callback 
    @api.doc(
        "Spotify Oauth2 Callback",
        responses={
            201: ("Successfully received callback"),
            401: ("Authentication required"),
            404: "User not found!",
        }
    )
    @api.expect(oauth_external, validate=True)
    @jwt_required
    #@api.doc(security=None)
    def post(self):
        """ Get access and refresh tokens """
        data = request.get_json()
        csrf = data['state']#request.args.get('state')
        user_uuid = get_jwt_identity() #decode_token(csrf)['identity']
        code = data['code'] #request.args.get('code')

        res = ExternalService.spotify_callback(csrf, code, user_uuid)
        thread = Thread(target=ExternalService.get_spotify_data, args=(
            user_uuid, current_app._get_current_object()))
        thread.daemon = True
        thread.start()
        return res

