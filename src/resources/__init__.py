from flask_restx import Api
from flask import Blueprint

from .auth_resource import api as auth_ns
from .group_resource import api as group_ns
from .user_resource import api as user_ns

from .application_resource import api as app_ns
from .book_resource import api as book_ns
from .game_resource import api as game_ns
from .movie_resource import api as movie_ns
from .serie_resource import api as serie_ns
from .track_resource import api as track_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="RecoFinement API", description="Main routes.", security='Bearer Auth', authorizations={
    'Bearer Auth': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    },
})

# API namespaces
api.add_namespace(auth_ns)
api.add_namespace(group_ns)
api.add_namespace(user_ns)

api.add_namespace(app_ns)
api.add_namespace(book_ns)
api.add_namespace(game_ns)
api.add_namespace(movie_ns)
api.add_namespace(serie_ns)
api.add_namespace(track_ns)
