import os
from dotenv import load_dotenv

load_dotenv()

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'postgresql://'+os.environ['DB_USER_LOGIN']+':'+os.environ['DB_USER_PASSWORD']+'@'+os.environ['DB_URL']+':'+os.environ['DB_PORT']+'/'+os.environ['DB_NAME']

DEBUG = os.environ['DEBUG_MODE']
PORT = os.environ['SERVICE_PORT']
