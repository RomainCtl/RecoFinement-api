import os
import datetime
from mailjet_rest import Client


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
    os.environ['DB_USER_LOGIN']+':'+os.environ['DB_USER_PASSWORD']+'@' + \
    os.environ['DB_URL']+':'+os.environ['DB_PORT']+'/'+os.environ['DB_NAME']

JWT_SECRET_KEY = os.environ['SECRET_KEY']
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=43_200)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access']

PORT = os.environ['SERVICE_PORT']

PAGE_SIZE = 24

# MAILJET
API_KEY = os.environ['MJ_APIKEY_PUBLIC']
API_SECRET = os.environ['MJ_APIKEY_PRIVATE']
MAILJET = Client(auth=(API_KEY, API_SECRET), version='v3.1')
FROM_EMAIL = "advise.ly1@gmail.com"
URL_FRONT = os.environ['URL_FRONT']

# SPOTIFY
SPOTIFY_PROVIDER = "https://accounts.spotify.com/authorize"
SPOTIFY_CLIENT_ID = os.environ['SPOTIFY_CLIENT_ID']
SPOTIFY_CLIENT_SECRET = os.environ['SPOTIFY_CLIENT_SECRET']
SPOTIFY_REDIRECT_URI = 'http://localhost:4040/api/external/spotify/callback'
SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY_SCOPE = 'user-library-read user-top-read playlist-read-private user-read-recently-played'
SPOTIFY_USER_URL = 'https://api.spotify.com/v1/me/'
