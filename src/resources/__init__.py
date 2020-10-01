from flask_restx import Api
from flask import Blueprint

from .auth_resource import api as auth_ns
from .group_resource import api as group_ns
from .track_resource import api as track_ns
from .user_resource import api as user_ns

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
api.add_namespace(track_ns)
api.add_namespace(user_ns)
