from settings import SPOTIFY_PROVIDER, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_URL_TOKEN, SPOTIFY_SCOPE, SPOTIFY_USER_URL
from urllib.parse import urlencode
import base64
import requests
import dateutil.parser
from flask_jwt_extended import create_access_token


class Spotify:
    @staticmethod
    def oauth_url(user):
        access_token = create_access_token(identity=user)
        params = urlencode({
            'client_id': SPOTIFY_CLIENT_ID,
            'scope': SPOTIFY_SCOPE,
            'redirect_uri': SPOTIFY_REDIRECT_URI,
            'response_type': 'code',
            'state': access_token
        })

        url = SPOTIFY_PROVIDER + '?' + params
        return url

    @staticmethod
    def get_tokens(code):
        payload = {
            'grant_type': 'authorization_code',
            'code': code,
            'redirect_uri': SPOTIFY_REDIRECT_URI
        }
        auth_header = base64.b64encode(
            (SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode('ascii'))
        headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

        response = requests.post(
            SPOTIFY_URL_TOKEN, data=payload, headers=headers)

        return response.json()

    @staticmethod
    def refresh_token(refresh_token):

        payload = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        auth_header = base64.b64encode(
            (SPOTIFY_CLIENT_ID + ':' + SPOTIFY_CLIENT_SECRET).encode('ascii'))
        headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

        response = requests.post(
            SPOTIFY_URL_TOKEN, data=payload, headers=headers)

        return response.json()

    """ @staticmethod
    def get_user_top_artist(access_token):
        limit = 20
        access_token = access_token  # your function to pull the token
        # from the place where you saved it
        items_list = []
        url = SPOTIFY_USER_URL + f"top/artists?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token}
        all_loaded = False
        while not all_loaded:
            response = requests.get(url, headers=headers).json()
            items = response['items']
            for item in items:
                elements = {}
                elements['genres'] = item['genres']
                elements['artist_name'] = item['name']
                items_list.append(elements)
            if response['next']:
                url = response['next']  # + f"&access_token={access_token}"
            else:
                all_loaded = True
        return items_list
    """
    @staticmethod
    def get_user_top_track(access_token):
        limit = 20

        items_list = []
        url = SPOTIFY_USER_URL + f"top/tracks?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token}
        all_loaded = False
        while not all_loaded:
            response = requests.get(url, headers=headers).json()
            items = response['items']
            for item in items:
                elements = {}
                elements['artist_name'] = []
                elements['release'] = item['album']['name']
                if isinstance(item['album']['images'], list) and len(item['album']['images']) > 0:
                    elements['cover_art_url'] = item['album']['images'][0]["url"] if (isinstance(
                        item['album']['images'], list) and len(item['album']['images']) > 0) else None
                else:
                    elements['cover_art_url'] = None
                elements['year'] = item['album']['release_date'].split(
                    "-")[0] if item['album']['release_date'] is not None else None
                for artist in item['artists']:
                    elements['artist_name'].append(artist['name'])
                elements['artist_name'] = " & ".join(elements['artist_name'])
                elements['title'] = item['name']
                elements['spotify_id'] = item['id']
                elements['played_at'] = None
                items_list.append(elements)
            if response['next']:
                url = response['next']
            else:
                all_loaded = True
        return items_list

    @staticmethod
    def get_user_recently_played(access_token):
        limit = 20
        items_list = []
        url = SPOTIFY_USER_URL + f"player/recently-played?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token}
        all_loaded = False
        while not all_loaded:
            response = requests.get(url, headers=headers).json()
            items = response['items']
            for item in items:
                elements = {}
                elements['artist_name'] = []
                elements['title'] = item['track']['name']
                elements['spotify_id'] = item['track']['id']
                elements['release'] = item['track']['album']['name']
                elements['year'] = item['track']['album']['release_date'].split(
                    "-")[0] if item['track']['album']['release_date'] is not None else None
                elements['played_at'] = dateutil.parser.isoparse(
                    item['played_at'][:-1]) if "played_at" in item.keys() else None
                for artist in item['track']['artists']:
                    elements['artist_name'].append(artist['name'])
                elements['artist_name'] = " & ".join(elements['artist_name'])
                url_cover = requests.get(
                    item['track']['href'], headers=headers).json()
                elements['cover_art_url'] = url_cover['album']['images'][0]['url'] if (isinstance(
                    url_cover['album']['images'], list) and len(url_cover['album']['images']) > 0) else None
                items_list.append(elements)
            if response['next']:
                url = response['next']
            else:
                all_loaded = True
        return items_list

    @staticmethod
    def get_user_playlist(access_token):
        limit = 20
        items_list = []
        url = SPOTIFY_USER_URL + f"playlists?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token}
        all_loaded = False
        while not all_loaded:
            response = requests.get(url, headers=headers).json()
            items = response['items']
            for item in items:
                elements = {}
                elements['tracks'] = []
                url_playlist = requests.get(
                    item['href'], headers=headers).json()
                elements['cover_art_url'] = url_playlist['images'][0]['url'] if (isinstance(
                    url_playlist['images'], list) and len(url_playlist['images']) > 0) else None
                elements['playlist_name'] = url_playlist['name']
                for track in url_playlist["tracks"]["items"]:
                    tk = {}
                    tk['artist_name'] = []
                    tk['release'] = track['track']['album']['name']
                    tk['cover_art_url'] = track['track']['album']['images'][0]["url"] if (isinstance(
                        track['track']['album']['images'], list) and len(track['track']['album']['images']) > 0) else None
                    tk['year'] = track['track']['album']['release_date'].split(
                        "-")[0] if track['track']['album']['release_date'] is not None else None
                    for artist in track['track']['artists']:
                        tk['artist_name'].append(artist['name'])
                    tk['artist_name'] = " & ".join(tk['artist_name'])
                    tk['title'] = track['track']['name']
                    tk['spotify_id'] = track['track']['id']
                    tk['played_at'] = None
                    elements['tracks'].append(tk)
                items_list.append(elements)
            if response['next']:
                url = response['next']
            else:
                all_loaded = True
        return items_list
