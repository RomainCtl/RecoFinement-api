from flask_restx import Api
from flask import Blueprint

from .application.controller import api as app_ns
from .auth.controller import api as auth_ns
from .book.controller import api as book_ns
from .game.controller import api as game_ns
from .track.controller import api as track_ns
from .user.controller import api as user_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="RecoFinement API", description="Main routes.", security=["ApiKey", "ApiKeyCSRF"], authorizations={
    'ApiKey': {
        'type': 'apiKey',
        'in': 'cookie',
        'name': 'access_token_cookie'
    },
    # we need to recover the 'csrf_access_token' cookie by ourself on swagger: https://github.com/python-restx/flask-restx/issues/96
    'ApiKeyCSRF': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'X-CSRF-TOKEN'
    }
})

# API namespaces
api.add_namespace(app_ns)
api.add_namespace(auth_ns)
api.add_namespace(book_ns)
api.add_namespace(game_ns)
api.add_namespace(track_ns)
api.add_namespace(user_ns)
