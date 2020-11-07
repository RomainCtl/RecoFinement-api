from settings import TMDB_PROVIDER, TMDB_CLIENT_TOKEN, TMDB_REDIRECT_URI, TMDB_URL_TOKEN, TMDB_SCOPE, TMDB_USER_URL,TMDB_USER_APPROVAL
from urllib.parse import urlencode
import base64
import requests
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token

class TMDB : 
    @staticmethod
    def oauth_url():
        
        response = requests.get(TMDB_PROVIDER,params={"api_key":TMDB_CLIENT_TOKEN})
        request_token = response.json()['request_token']
                    
        return  TMDB_USER_APPROVAL+request_token+"?redirect_to="+TMDB_REDIRECT_URI
    
    @staticmethod
    def get_tokens(request_token):

        payload = {
            "request_token" : request_token
        }       
        response = requests.post(TMDB_URL_TOKEN+TMDB_CLIENT_TOKEN, data=payload)

        return response.json()
    
    @staticmethod
    def get_account_id(session_id):
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id
            }
        return requests.get(TMDB_USER_URL+"account",params=params)
