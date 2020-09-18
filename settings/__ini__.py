import os
from dotenv import load_dotenv

load_dotenv()

MYSQL_DATABASE_CHARSET = 'utf8'
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_POOL_RECYCLE = 3600 # this setting causes the pool to recycle connections after the given number of seconds has passed
SQLALCHEMY_POOL_TIMEOUT = 20 # number of seconds to wait before giving up on getting a connection from the pool
SQLALCHEMY_POOL_SIZE = 1 # the number of connections to keep open inside the connection pool

SQLALCHEMY_DATABASE_URI = 'mysql://'+os.environ['DB_USER_LOGIN']+':'+os.environ['DB_USER_PASSWORD']+'@'+os.environ['DB_URL']+':'+os.environ['DB_PORT']+'/'+os.environ['DB_NAME']

DEBUG = os.environ['DEBUG_MODE']
PORT = os.environ['SERVICE_PORT']
