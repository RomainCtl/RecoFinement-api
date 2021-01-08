from flask_restx import Namespace, fields

from .base import ApplicationBaseObj, GenreBaseObj, paginationObj, messageObj, MetaUserContentBaseObj


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
