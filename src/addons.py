from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

from flask_bcrypt import Bcrypt
from flask_cors import CORS
from flask_jwt_extended import JWTManager

db = SQLAlchemy()

bcrypt = Bcrypt()
migrate = Migrate(compare_type=True)
cors = CORS()

jwt = JWTManager()
ma = Marshmallow()
