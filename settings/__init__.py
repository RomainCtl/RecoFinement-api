import os
import datetime
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://' + \
    os.environ['DB_USER_LOGIN']+':'+os.environ['DB_USER_PASSWORD']+'@' + \
    os.environ['DB_URL']+':'+os.environ['DB_PORT']+'/'+os.environ['DB_NAME']

JWT_SECRET_KEY = os.environ['SECRET_KEY']
JWT_ACCESS_TOKEN_EXPIRES = datetime.timedelta(seconds=43_200)
JWT_BLACKLIST_ENABLED = True
JWT_BLACKLIST_TOKEN_CHECKS = ['access']

JWT_COOKIE_SECURE = False  # Only allow JWT cookies to be sent over https.

PORT = os.environ['SERVICE_PORT']

PAGE_SIZE = 20
