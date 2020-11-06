from settings import SPOTIFY_PROVIDER, TMDB_PROVIDER, TMDB_CLIENT_TOKEN, TMDB_REDIRECT_URI, TMDB_URL_TOKEN, TMDB_SCOPE, TMDB_USER_URL,TMDB_USER_APPROVAL
from urllib.parse import urlencode
import base64
import requests
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token

class TMDB :
    @staticmethod
    def oauth_url():
        payload = {
            "redirect_to" : "http://localhost:4200/recofinement"
        }
        headers = {
        'content-type': "application/json;charset=utf-8",
        'authorization': "Bearer "+ TMDB_CLIENT_TOKEN
        }
        response = requests.post(SPOTIFY_PROVIDER, data=payload, headers=headers)
        print(response)
        resquest_token = response.text['request_token']
                    
        url = TMDB_USER_APPROVAL + resquest_token
        return url