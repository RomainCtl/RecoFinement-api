from settings import TMDB_PROVIDER, TMDB_CLIENT_TOKEN, TMDB_REDIRECT_URI, TMDB_URL_TOKEN, TMDB_IMG_URL, TMDB_USER_URL,TMDB_USER_APPROVAL
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
        #  "id": 9802731
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id
            }
        return requests.get(TMDB_USER_URL+"account",params=params).json()['id']
        
    
    
    @staticmethod
    def get_movies(item,element):
        element['title']=item['title']
        element['language'] = item['original_language']
        element['year'] = item['release_date']
        
        element['tmdbid'] = item['id']
        element['rating'] = float(item['vote_average']*5/10.0)
        element['rating_count'] = item['vote_count']
        element['cover'] = TMDB_IMG_URL + item['poster_path']
        return element

    @staticmethod
    def get_movies_details(id,element):
        details = requests.get(TMDB_USER_URL+f"movie/{id}",{"api_key" : TMDB_CLIENT_TOKEN}).json()
                
        element['imdbid'] = details['imdb_id'][2:]
        element['genres'] = []
        for genre in details['genres']:
            element['genres'].append(genre['name'])
        element['genres'] = ("|").join(element['genres'])
        
        credits = requests.get(TMDB_USER_URL+f"movie/{id}/credits",{"api_key" : TMDB_CLIENT_TOKEN}).json()

        element['actors'] = []
        for actors in credits['cast'] :
            element['actors'].append(actors['name'])
            if actors['order'] == 4:
                break
        element['actors'] = (" | ").join(element['actors'])
        element['producers'] = []
        element['director'] = ''
        element['writer'] = ''
        for crew in credits['crew'] :
            if len(element['producers']) < 5:
                element['producers'].append(crew['name']) if crew['department']=="Production" else None
            if len(element['director']) < 1 and (crew['department'] == "Directing") :
                element['director'] = crew['name']
            if len(element['writer']) < 1 and ( crew['department'] == "Writing"):
                element['writer'] = crew['name']
            if len(element['producers']) == 5 and len(element['director']) >= 1 and len(element['writer']) >= 1:
                break
        element['producers'] = (' | ').join(element['producers'])
        return element

    

    @staticmethod
    def get_series(item,element):
        element['title'] = item['original_name']
        #element['language'] = item['originial_language']
        element['start_year'] = int(item['first_air_date'][:4])
        element['rating'] = float(item['vote_average']*5/10.0)
        element['rating_count'] = item['vote_count']
        element['cover'] = TMDB_IMG_URL + item['poster_path']
        return element

    @staticmethod
    def get_series_details(id,element):
        details = requests.get(TMDB_USER_URL+f"tv/{id}",{"api_key" : TMDB_CLIENT_TOKEN}).json()
                
        element['end_year'] = int(details['last_air_date'][:4])
        element['genres'] = []
        for genre in details['genres']:
            element['genres'].append(genre['name'])
        element['genres'] = (",").join(element['genres'])
        
        credits = requests.get(TMDB_USER_URL+f"tv/{id}/credits",{"api_key" : TMDB_CLIENT_TOKEN}).json()

        element['actors'] = []
        for actors in credits['cast'] :
            element['actors'].append(actors['name'])
            if actors['order'] == 4:
                break
        element['actors'] = (",").join(element['actors'])
        element['directors'] = []
        element['writers'] = []
        for crew in credits['crew'] :
            if len(element['directors']) < 2 and ( crew['department']== "Directing" ):
                element['directors'].append(crew['name'])
            if len(element['writers']) < 4 and (crew['department'] == "Writing"):
                element['writers'].append(crew['name'])
            if  (len(element['directors']) == 2) and (len(element['writers']) == 4):
                break
        element['directors'] = (',').join(element['directors'])
        element['writers'] = (',').join(element['writers'])
        return element


    @staticmethod
    def get_favorite_movies(session_id,account_id):
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id,
            "sort_by" : "created_at.asc",
            "page" : 1
            }
        response = requests.get(TMDB_USER_URL+f"account/{account_id}/favorite/movies",params=params).json()
        
        data = []
        pages = response['total_pages']
        for page in range(0,pages):
            for item in response["results"]:
                element = {}
                element=TMDB.get_movies(item,element)
                
                element = TMDB.get_movies_details(item['id'],element)
                data.append(element)
            params['page']=page+1
            response = requests.get(TMDB_USER_URL+f"account/{account_id}/favorite/movies",params=params).json()
        
        return data

    @staticmethod
    def get_favorite_series(session_id,account_id):
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id,
            "sort_by" : "created_at.asc",
            "page" : 1
            }
        response = requests.get(TMDB_USER_URL+f"account/{account_id}/favorite/tv",params=params).json()
        data = []
        pages = response['total_pages']
        for page in range(0,pages):
            for item in response["results"]:
                element = {}
                element = TMDB.get_series(item,element)
                
                element = TMDB.get_series_details(item['id'],element)
                data.append(element)
            params['page']=page+1
            response = requests.get(TMDB_USER_URL+f"account/{account_id}/favorite/tv",params=params).json()
        
        return data

    @staticmethod
    def get_rated_movies(session_id, account_id):
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id,
            "sort_by" : "created_at.asc",
            "page" : 1
            }
        response = requests.get(TMDB_USER_URL+f"account/{account_id}/rated/movies",params=params).json()
        data = []
        pages = response['total_pages']
        for page in range(0,pages):
            for item in response["results"]:
                element = {}
                element = TMDB.get_movies(item,element)
                element['user_rating'] = round(float(item['rating']*5/10.0)*2)/2
                
                element = TMDB.get_movies_details(item['id'],element)
                data.append(element)
            params['page']=page+1
            response = requests.get(TMDB_USER_URL+f"account/{account_id}/rated/movies",params=params).json()
        
        return data

    @staticmethod
    def get_rated_series(session_id, account_id):
        params= {
            "api_key" : TMDB_CLIENT_TOKEN,
            "session_id" : session_id,
            "sort_by" : "created_at.asc",
            "page" : 1
            }
        response = requests.get(TMDB_USER_URL+f"account/{account_id}/rated/tv",params=params).json()
        data = []
        pages = response['total_pages']
        for page in range(0,pages):
            for item in response["results"]:
                element = {}
                element = TMDB.get_series(item,element)
                element['user_rating'] = round(float(item['rating']*5/10.0)*2)/2
                element = TMDB.get_series_details(item['id'],element)
                data.append(element)
            params['page']=page+1
            response = requests.get(TMDB_USER_URL+f"account/{account_id}/rated/tv",params=params).json()
        
        return data

    @staticmethod
    def get_created_list(session_id,account_id):
        params= {
        "api_key" : TMDB_CLIENT_TOKEN,
        "session_id" : session_id,
        "page" : 1
        }
        response = requests.get(TMDB_USER_URL+f"account/{account_id}/lists",params=params).json()
        movies = []
        series = []
        pages = response['total_pages']
        for page in range(0,pages):
            for item in response["results"]:
                userlist = requests.get(TMDB_USER_URL+f"list/{item['id']}",params={"api_key" : TMDB_CLIENT_TOKEN}).json()
                for item in userlist['items']:
                    element = {}
                    if item['media_type'] == 'tv' :
                        element = TMDB.get_series(item,element)
                        element = TMDB.get_series_details(item['id'],element)
                        series.append(element)
                    elif item['media_type'] == 'movie' :
                        element = TMDB.get_movies(item,element)
                        element = TMDB.get_movies_details(item['id'],element)
                        movies.append(element)
            params['page']=page+1
            response = requests.get(TMDB_USER_URL+f"account/{account_id}/rated/tv",params=params).json()
        
        return {
            "movies" : movies,
            "series" : series
            }