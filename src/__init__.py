from flask import Flask
from jwt import ExpiredSignatureError

from src.addons import db, ma, migrate, cors, bcrypt, jwt, flask_uuid
from src.utils import err_resp
import settings


def create_app(config=None):
    """
    Create application
    """
    #: Flask application
    app = Flask(__name__)
    if config is None:
        app.config.from_object(settings)
    else:
        app.config.from_object(config)

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

    @app.errorhandler(ExpiredSignatureError)
    def handle_expired_token(e):
        return err_resp('The token has expired', 401)

    # Register blueprints
    from .resources import api_bp

    app.register_blueprint(api_bp, url_prefix="/api")

    return app
