from flask_restx import Api
from flask import Blueprint

from .auth.controller import api as auth_ns
from .user.controller import api as user_ns
from .track.controller import api as track_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="RecoFinement API", description="Main routes.")

# API namespaces
api.add_namespace(auth_ns)
api.add_namespace(user_ns)
api.add_namespace(track_ns)
