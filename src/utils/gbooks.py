from flask_jwt_extended import create_access_token
import json

from settings import GBOOKS_TOKEN_URI, GOOGLE_OAUTH_FILE, GBOOKS_SCOPES, GBOOKS_REDIRECT_URL
from googleapiclient.discovery import build
from google_auth_oauthlib.flow import Flow
from google.auth.transport.requests import Request
import google.oauth2.credentials


def credentials_to_dict(credentials):
    return {'token': credentials.token,
            'refresh_token': credentials.refresh_token,
            'token_uri': credentials.token_uri,
            'client_id': credentials.client_id,
            'client_secret': credentials.client_secret,
            'scopes': credentials.scopes}


class GBooks:
    @staticmethod
    def oauth_url(user):
        access_token = create_access_token(identity=user)
        flow = Flow.from_client_secrets_file(GOOGLE_OAUTH_FILE, GBOOKS_SCOPES)
        flow.redirect_uri = GBOOKS_REDIRECT_URL
        url, _ = flow.authorization_url(
            access_type='offline',
            include_granted_scopes='true',
            state=access_token
        )
        return url

    @staticmethod
    def get_token(code, state):
        flow = Flow.from_client_secrets_file(
            GOOGLE_OAUTH_FILE, GBOOKS_SCOPES, state=state)
        flow.redirect_uri = GBOOKS_REDIRECT_URL
        # Use the authorization server's response to fetch the OAuth 2.0 tokens.
        flow.fetch_token(code=code)

        credentials = flow.credentials
        return credentials_to_dict(credentials)

    @staticmethod
    def get_data(token, refresh_token):
        rating = {
            "ONE": 1,
            "TWO": 2,
            "THREE": 3,
            "FOUR": 4,
            "FIVE": 5
        }
        # Load credentials from the session.
        with open(GOOGLE_OAUTH_FILE) as json_file:
            data = json.load(json_file)
        credentials = google.oauth2.credentials.Credentials(
            token=token,
            refresh_token=refresh_token,
            token_uri=data['web']['token_uri'],
            client_id=data['web']['client_id'],
            client_secret=data['web']['client_secret'],
            scopes=GBOOKS_SCOPES
        )
        try:
            credentials.refresh(Request())
        except Exception:
            return "revoked"
        books = build('books', 'v1', credentials=credentials)
        bookshelves = books.mylibrary().bookshelves().list().execute()
        excludedShelves = ['To read', 'Books for you',
                           'Browsing history', 'Recently viewed']
        data = []
        # return bookshelves
        shelf_id = []
        for bs in bookshelves['items']:
            if bs["title"] not in excludedShelves and "volumeCount" in bs.keys() and bs['volumeCount'] != 0:
                if bs['title'] == "Reviewed":
                    shelf_id.insert(0, bs['id'])
                else:
                    shelf_id.append(bs['id'])
            for id in shelf_id:
                for user_bk in books.mylibrary().bookshelves().volumes().list(shelf=str(id), projection='FULL').execute()["items"]:
                    # return bk # ! change shelf to bs['id']

                    # ? if get description take same link as "publisher"
                    """ bk = books.volumes().get(volumeId=str('0i_BjgEACAAJ')).execute()
                    return bk  """
                    if ("industryIdentifiers" in user_bk['volumeInfo'].keys()):
                        for isbn in user_bk["volumeInfo"]["industryIdentifiers"]:
                            if isbn['type'] == "ISBN_13":
                                element = {}
                                if "userInfo" in user_bk.keys():
                                    if "review" in user_bk['userInfo'].keys() and "rating" in user_bk['userInfo']['review'].keys() and user_bk['userInfo']['review']['rating'] != "NOT_RATED":
                                        element['user_rating'] = rating[user_bk['userInfo']
                                                                        ['review']['rating']]
                                    else:
                                        element['user_rating'] = None
                                    if "isPurchased" in user_bk['userInfo'].keys():
                                        element['purchase'] = user_bk['userInfo']["isPurchased"]
                                    else:
                                        element['purchase'] = None
                                bk = books.volumes().get(
                                    volumeId=str(user_bk['id'])).execute()
                                element["isbn"] = isbn['identifier']
                                element["title"] = bk['volumeInfo']['title']
                                element["author"] = bk['volumeInfo']['authors'][0] if (isinstance(
                                    bk['volumeInfo']['authors'], list) and len(bk['volumeInfo']['authors']) > 0) else None
                                element["year_of_publication"] = bk['volumeInfo']['publishedDate'][:4]
                                element["publisher"] = bk['volumeInfo']['publisher']
                                if "imageLinks" in bk["volumeInfo"].keys():
                                    if "small" in bk['volumeInfo']['imageLinks'].keys() and "medium" in bk['volumeInfo']['imageLinks'].keys() and "large" in bk['volumeInfo']['imageLinks'].keys():
                                        element["image_url_s"] = bk['volumeInfo']['imageLinks']['small']
                                        element["image_url_m"] = bk['volumeInfo']['imageLinks']['medium']
                                        element["image_url_l"] = bk['volumeInfo']['imageLinks']['large']
                                    else:
                                        try:
                                            img = bk['volumeInfo']['imageLinks']
                                            element["image_url_s"] = next(
                                                iter(img.values()))
                                            element["image_url_m"] = next(
                                                iter(img.values()))
                                            element["image_url_l"] = next(
                                                iter(img.values()))
                                        except:
                                            element["image_url_s"] = None
                                            element["image_url_m"] = None
                                            element["image_url_l"] = None
                                else:
                                    element["image_url_s"] = None
                                    element["image_url_m"] = None
                                    element["image_url_l"] = None
                                if "averageRating" in bk['volumeInfo'].keys():
                                    element["rating"] = bk['volumeInfo']['averageRating']
                                    element["rating_count"] = bk['volumeInfo']['ratingsCount']
                                else:
                                    element["rating"] = None
                                    element["rating_count"] = None
                                data.append(element)
        return data
