from flask_restx import Namespace, fields

from .base import SerieBaseObj, SerieItemObj, paginationObj, messageObj, GenreBaseObj


class SerieDto:
    api = Namespace("serie", description="Serie related operations.")

    # Objects
    api.models[SerieBaseObj.name] = SerieBaseObj
    serie_base = SerieBaseObj

    api.models[SerieItemObj.name] = SerieItemObj
    serie_item = SerieItemObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    # Responses
    data_resp = api.clone(
        "Serie list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(serie_base)),
        },
    )

    u_data_resp = api.clone(
        "Serie Data Response",
        messageObj,
        {
            "serie": fields.List(fields.Nested(serie_item)),
        },
    )

    genres_resp = api.clone(
        "Serie genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )
