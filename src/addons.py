from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_uuid import FlaskUUID
from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

from flask_socketio import SocketIO

db = SQLAlchemy()

bcrypt = Bcrypt()
migrate = Migrate(compare_type=True)
cors = CORS()
flask_uuid = FlaskUUID()

jwt = JWTManager()
ma = Marshmallow()

socketio = SocketIO()
