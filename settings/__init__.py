import os
import datetime
from dotenv import load_dotenv
from mailjet_rest import Client


load_dotenv()

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

API_KEY = os.environ['MJ_APIKEY_PUBLIC']
API_SECRET = os.environ['MJ_APIKEY_PRIVATE']
MAILJET = Client(auth=(API_KEY, API_SECRET), version='v3.1')
FROM_EMAIL="advise.ly1@gmail.com"