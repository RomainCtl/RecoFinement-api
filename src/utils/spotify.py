from settings import SPOTIFY_PROVIDER, SPOTIFY_CLIENT_ID, SPOTIFY_CLIENT_SECRET, SPOTIFY_REDIRECT_URI, SPOTIFY_URL_TOKEN, SPOTIFY_SCOPE, SPOTIFY_USER_URL
from urllib.parse import urlencode
import base64
import requests
from flask_jwt_extended import create_access_token, set_access_cookies, decode_token


class Spotify:
    @staticmethod
    def oauth_url(uuid):
        access_token = create_access_token(identity=uuid)
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
                'code' : code,
                'redirect_uri' : SPOTIFY_REDIRECT_URI
            }
        # TODO check state 
        auth_header = base64.b64encode((SPOTIFY_CLIENT_ID+ ':' + SPOTIFY_CLIENT_SECRET).encode('ascii'))
        headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}
        
        response = requests.post(SPOTIFY_URL_TOKEN, data=payload, headers=headers)

        return response.json()
    
    @staticmethod
    def refresh_token(refresh_token):
        
        payload = {
            'refresh_token': refresh_token,
            'grant_type': 'refresh_token'
        }

        auth_header = base64.b64encode((SPOTIFY_CLIENT_ID+ ':' + SPOTIFY_CLIENT_SECRET).encode('ascii'))
        headers = {'Authorization': 'Basic %s' % auth_header.decode('ascii')}

        response = requests.post(SPOTIFY_URL_TOKEN, data=payload, headers=headers)

        return response.json()

    
    @staticmethod
    def get_user_top_artist(access_token):
        limit = 20
        access_token = access_token # your function to pull the token
                                            # from the place where you saved it
        items_list = []
        url = SPOTIFY_USER_URL+ f"top/artists?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token }
        all_loaded = False
        while not all_loaded:
            response = requests.get(url,headers=headers).json()
            '''  if "error" in response.keys() and 401 == response['error']['status']:
                Spotify.refresh_token(refresh_token) # TODO
                response = requests.get(url) '''
            items = response['items']
            for item in items:
                elements = {}
                elements['genres'] = item['genres']
                elements['artist_name'] = item['name']
                items_list.append(elements)
            if response['next']:
                url = response['next']# + f"&access_token={access_token}"
            else:
                all_loaded = True
        return items_list
    
    @staticmethod
    def get_user_top_track(access_token):
        limit = 20

        items_list = []
        url = SPOTIFY_USER_URL+ f"top/tracks?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token }
        all_loaded = False
        while not all_loaded:
            response = requests.get(url,headers=headers).json()
            ''' if "error" in response.keys() and 401 == response['error']['status']:
                Spotify.refresh_token(refresh_token) # TODO
                response = requests.get(url) '''
            items = response['items']
            for item in items:
                elements = {}
                elements['artist_name']=[]
                elements['release'] = item['album']['name']
                elements['cover_art_url'] = item['album']['images'][0]["url"]
                elements['year'] = item['album']['release_date']
                for artist in item['artists']:
                    elements['artist_name'].append(artist['name'])
                elements['title'] = item['name']
                elements['spotify_id'] = item['id']
                items_list.append(elements)
            if response['next']:
                url = response['next']
            else:
                all_loaded = True
        return items_list
    
    @staticmethod
    def get_user_album_saved(access_token):
        limit = 20
        items_list = []
        url = SPOTIFY_USER_URL+ f"top/tracks?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token }
        all_loaded = False
        while not all_loaded:
            response = requests.get(url,headers=headers).json()
            ''' if "error" in response.keys() and 401 == response['error']['status']:
                Spotify.refresh_token(refresh_token) # TODO
                response = requests.get(url) '''
            items = response['items']
            for item in items:
                elements = {}
                elements['artist_name']=[]
                elements['release'] = item['album']['name']
                elements['cover_art_url'] = item['album']['images'][0]["url"]
                elements['year'] = item['album']['release_date']
                for artist in item['artists']:
                    elements['artist_name'].append(artist['name'])
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
        url = SPOTIFY_USER_URL+ f"player/recently-played?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token }
        all_loaded = False
        while not all_loaded:
            response = requests.get(url,headers=headers).json()
            ''' if "error" in response.keys() and 401 == response['error']['status']:
                Spotify.refresh_token(refresh_token) # TODO
                response = requests.get(url) '''
            items = response['items']
            for item in items:
                elements = {}
                elements['artist_name']=[]
                elements['title'] = item['track']['name']
                elements['spotify_id'] = item['track']['id']
                elements['release'] = item['track']['album']['name']
                elements['year'] = item['track']['album']['release_date']
                elements['played_at'] = item['played_at']
                for artist in item['track']['artists']:
                    elements['artist_name'].append(artist['name'])
                url_cover = requests.get(item['track']['href'],headers=headers).json()
                elements['cover_art_url'] = url_cover['album']['images'][0]['url']
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
        url = SPOTIFY_USER_URL+ f"playlists?limit={limit}"
        headers = {'Authorization': "Bearer "+access_token }
        all_loaded = False
        while not all_loaded:
            response = requests.get(url,headers=headers).json()
            ''' if "error" in response.keys() and 401 == response['error']['status']:
                Spotify.refresh_token(refresh_token) # TODO
                response = requests.get(url) '''
            items = response['items']
            for item in items:
                elements = {}
                elements['tracks']=[]
                url_playlist = requests.get(item['href'],headers=headers).json()
                elements['cover_art_url'] = url_playlist['images'][0]['url']
                elements['playlist_name'] = url_playlist['name']
                for track in url_playlist["tracks"]["items"]:
                    tk={}
                    tk['artist_name']=[]
                    tk['release'] = track['track']['album']['name']
                    tk['cover_art_url'] = track['track']['album']['images'][0]["url"]
                    tk['year'] = track['track']['album']['release_date']
                    for artist in track['track']['artists']:
                        tk['artist_name'].append(artist['name'])
                    tk['title'] = track['track']['name']
                    tk['spotify_id'] = track['track']['id']
                    elements['tracks'].append(tk)
                items_list.append(elements)
            if response['next']:
                url = response['next']
            else:
                all_loaded = True
        return items_list