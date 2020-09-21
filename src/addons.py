from flask import Flask
from flask_restx import Api
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#: Flask application
app = Flask(__name__)

api = Api()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate(compare_type=True)
