from flask_restx import Namespace, fields

from .base import ApplicationBaseObj, GenreBaseObj, paginationObj, messageObj, MetaUserContentBaseObj
from .base import ApplicationAdditionalBaseObj

class ApplicationDto:
    api = Namespace(
        "application", description="Application related operations.")

    # Objects
    api.models[ApplicationBaseObj.name] = ApplicationBaseObj
    app_base = ApplicationBaseObj

    # Responses
    data_resp = api.clone(
        "Application list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(app_base)),
        },
    )

    application_bad_recommendation = api.model(
        "ApplicationBadRecommendationMetaExpected",
        {
            "categorie": fields.List(fields.String)
        }
    )

class ApplicationAdditionalDto:
    api = Namespace("application_additional", description="Additional application related operations.")

    #Objects
    api.models[ApplicationAdditionalBaseObj.name] = ApplicationAdditionalBaseObj
    application_additional_base = ApplicationAdditionalBaseObj 