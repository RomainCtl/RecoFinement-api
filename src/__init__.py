from flask import Flask
import os

from src.addons import db, ma, migrate, cors, bcrypt, jwt, flask_uuid
import settings


def create_app():
    """
    Create application
    """
    #: Flask application
    app = Flask(__name__)
    app.config.from_object(settings)

    # Registers flask extensions
    db.init_app(app)
    ma.init_app(app)
    jwt.init_app(app)
    bcrypt.init_app(app)
    cors.init_app(app, resources={r"*": {"origins": "*"}})
    migrate.init_app(app, db=db)
    flask_uuid.init_app(app)

    # JWT overrided method
    from .model import RevokedTokenModel

    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        return RevokedTokenModel.is_revoked(decrypted_token['jti'])

    # Register blueprints
    from .resources import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
