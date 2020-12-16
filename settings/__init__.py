import os
import datetime
from mailjet_rest import Client


SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
    os.environ.get('DB_USER_LOGIN', '')+':'+os.environ.get('DB_USER_PASSWORD', '')+'@' + \
    os.environ.get('DB_URL', '')+':'+os.environ.get('DB_PORT', '')+'/'+os.environ.get('DB_NAME', '')

JWT_SECRET_KEY = os.environ.get('SECRET_KEY', '')
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=43_200)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access']

PORT = os.environ.get('SERVICE_PORT', '')

ENGINE_URL = os.environ.get("ENGINE_URL", "http://127.0.0.1:4041")
ENGINE_APIKEY = os.environ.get("ENGINE_APIKEY", "")

PAGE_SIZE = 24

# MAILJET
API_KEY = os.environ.get('MJ_APIKEY_PUBLIC', '')
API_SECRET = os.environ.get('MJ_APIKEY_PRIVATE', '')
MAILJET = Client(auth=(API_KEY, API_SECRET), version='v3.1')
FROM_EMAIL = "advise.ly1@gmail.com"
URL_FRONT = os.environ.get('URL_FRONT', '')

# SPOTIFY
SPOTIFY_PROVIDER = "https://accounts.spotify.com/authorize"
SPOTIFY_CLIENT_ID = os.environ.get('SPOTIFY_CLIENT_ID', '')
SPOTIFY_CLIENT_SECRET = os.environ.get('SPOTIFY_CLIENT_SECRET', '')
SPOTIFY_REDIRECT_URI = URL_FRONT+'/recofinement/user/profile'
SPOTIFY_URL_TOKEN = "https://accounts.spotify.com/api/token"
SPOTIFY_SCOPE = 'user-library-read user-top-read playlist-read-private user-read-recently-played'
SPOTIFY_USER_URL = 'https://api.spotify.com/v1/me/'

# TMDB
TMDB_PROVIDER = "https://api.themoviedb.org/3/authentication/token/new"
TMDB_USER_APPROVAL = "https://www.themoviedb.org/authenticate/"
TMDB_CLIENT_TOKEN = os.environ.get('TMDB_CLIENT_TOKEN', '')
TMDB_REDIRECT_URI = URL_FRONT+'/recofinement/user/profile'
TMDB_URL_TOKEN = "https://api.themoviedb.org/3/authentication/session/new?api_key="
TMDB_IMG_URL = 'https://image.tmdb.org/t/p/w500/'
TMDB_USER_URL = 'https://api.themoviedb.org/3/'

# GOOGLE BOOKS
GOOGLE_OAUTH_FILE = os.environ.get('PATH_TO_GOOGLE_OAUTH_FILE', '')
GBOOKS_SCOPES = ['https://www.googleapis.com/auth/books']
GBOOKS_REDIRECT_URL = URL_FRONT+'/recofinement/user/profile'
GBOOKS_TOKEN_URI = "https://oauth2.googleapis.com/token"

# REASON CATEGORIES
REASON_CATEGORIES = {
    "book" : ["author","publisher","year_of_publication"],
    "application" : ["genre"],
    "game" : ["developers", "publishers", "genres", "release_date"],
    "movie" : ["actors", "year", "producers", "director", "genres", "writer"],
    "serie" : ["directors", "writers", "start_year", "end_year", "genres", "actors"],
    "track" : ["year", "artist_name", "release", "genres"]
}