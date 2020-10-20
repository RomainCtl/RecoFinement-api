from flask_restx import Namespace, fields

from .base import ApplicationBaseObj, GenreBaseObj, paginationObj, messageObj


class ApplicationDto:
    api = Namespace(
        "application", description="Application related operations.")

    # Objects
    api.models[ApplicationBaseObj.name] = ApplicationBaseObj
    app_base = ApplicationBaseObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    # Responses
    data_resp = api.clone(
        "Application list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(app_base)),
        },
    )

    genres_resp = api.clone(
        "Application genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    # Excepted data
    application_meta = api.model(
        "ApplicationMetaExpected",
        {
            "review": fields.String,
            "rating": fields.Integer(min=0, max=5),
            "downloaded": fields.Boolean,
        }
    )
