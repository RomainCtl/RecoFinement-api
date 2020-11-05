from settings import TMDB_PROVIDER, TMDB_CLIENT_ID, TMDB_CLIENT_SECRET, TMDB_REDIRECT_URI, TMDB_URL_TOKEN, TMDB_SCOPE, TMDB_USER_URL
from urllib.parse import urlencode
import base64
import requests
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token

class Tmdb :
    @staticmethod
    def oauth_url(uuid):
        access_token = create_access_token(identity=uuid)
        params = urlencode({
                    'client_id': TMDB_CLIENT_ID,
                    'scope': TMDB_SCOPE,
                    'redirect_uri': TMDB_REDIRECT_URI,
                    'response_type': 'code',
                    'state': access_token
                    })
                    
        url = TMDB_PROVIDER + '?' + params
        return url