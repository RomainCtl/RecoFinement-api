from flask_restx import Api
from flask import Blueprint

from .track.controller import api as track_ns

# Import controller APIs as namespaces.
api_bp = Blueprint("api", __name__)

api = Api(api_bp, title="RecoFinement API", description="Main routes.")

# API namespaces
api.add_namespace(track_ns)
