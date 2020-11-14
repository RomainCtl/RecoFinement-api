from flask_restx import Namespace, fields
from .base import ExternalBaseObj, messageObj



class ExternalDto:
    api = Namespace(
        "external", description="External services related operations.")

    # Objects
    api.models[ExternalBaseObj.name] = ExternalBaseObj
    external_base = ExternalBaseObj

    # Responses
    oauth_url = api.model(
        "External service auth success response",
        {
            **messageObj,
            "url": fields.String,
        },
    )

    # Expected tmdb data
    oauth_spotify_callback = api.model(
        "ExternalDataExpected",
        {
            "state": fields.String(min=300,max=350),
            "code": fields.String(min=10, max=350),
        },
    )

    # Expected tmdb data
    oauth_tmdb_callback = api.model(
        "ExternalDataExpected",
        {
            "request_token" : fields.String(min=10, max=350),
            "approved" : fields.Boolean,
            "denied" : fields.Boolean
        },
    )

    # Expected data
    oauth_gbooks_callback = api.model(
        "ExternalDataExpected",
        {
            "state" : fields.String(min=300, max=350),
            "code" : fields.String(min=50, max=85),
            "scope" : fields.String(min=38, max=38) #"https://www.googleapis.com/auth/books"
        },
    )