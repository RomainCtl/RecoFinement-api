from flask import Flask
from flask_restplus import API
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
from flask_migrate import Migrate

#: Flask application
app = Flask(__name__)

api = API()
db = SQLAlchemy()
ma = Marshmallow()
migrate = Migrate(compare_type=True)
