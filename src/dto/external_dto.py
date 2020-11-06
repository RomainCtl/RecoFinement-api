from flask_restx import Namespace, fields
from .base import ExternalBaseObj, messageObj

class ExternalDto:
    api = Namespace("external", description="External services related operations.")
    
    # Objects
    api.models[ExternalBaseObj.name] = ExternalBaseObj
    external_base = ExternalBaseObj
        
    # Responses
    oauth_url = api.model(
        "Auth success response",
        {
            **messageObj,
            "url": fields.String,
        },
    )
    
    #Expected data

    oauth_callback = api.model(
        "ExternalDataExpected",
        {
            "state": fields.String(min=10,max=350),
            "code": fields.String(min=10, max=350),
            "request_token" : fields.String(min=10, max=350),
            "approved" : fields.String(min=4, max=5),
        },
    )