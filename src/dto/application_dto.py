from flask_restx import Namespace, fields

from .base import ApplicationBaseObj, GenreBaseObj, paginationObj, messageObj, MetaUserContentBaseObj, ApplicationAdditionalBaseObj


class ApplicationDto:
    api = Namespace(
        "application", description="Application related operations.")

    # Objects
    api.models[ApplicationBaseObj.name] = ApplicationBaseObj
    app_base = ApplicationBaseObj

    api.models[ApplicationAdditionalBaseObj.name] = ApplicationAdditionalBaseObj
    application_additional_base = ApplicationAdditionalBaseObj

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
