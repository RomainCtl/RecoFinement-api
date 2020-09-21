from flask_cors import CORS
from dotenv import load_dotenv
import os

from src.addons import app, api, db, ma, migrate
import settings


def create_app():
    """
    Create application
    """
    cors = CORS(app, resources={r"/*": {"origins": "*"}})
    app.config.from_object(settings)

    with app.app_context():
        db.init_app(app)
        ma.init_app(app)

        migrate.init_app(app,db=db)

        api.init_app(app)

    # api.add_resource(HomeResource, '/', '/home', endpoint="home")

    # api.add_resource(MusicResource, /music', endpoint="music_all")
    # api.add_resource(MusicResource, /music/<int:msc_id>', endpoint="music_by_id")

    return app
