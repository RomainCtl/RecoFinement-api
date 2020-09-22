from flask import Flask

from src.addons import db, ma, migrate, cors, bcrypt, jwt
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
    cors.init_app(app)
    migrate.init_app(app,db=db)

    # JWT overrided method
    from .model import RevokedToken
    @jwt.token_in_blacklist_loader
    def check_if_token_is_revoked(decrypted_token):
        return RevokedToken.is_revoked(decrypted_token['jti'])

    # Register blueprints
    from .resources import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
