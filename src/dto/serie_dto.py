from flask_restx import Namespace, fields

from .base import SerieBaseObj, SerieItemObj, paginationObj, messageObj


class SerieDto:
    api = Namespace("serie", description="Serie related operations.")

    # Objects
    api.models[SerieBaseObj.name] = SerieBaseObj
    serie_base = SerieBaseObj

    api.models[SerieItemObj.name] = SerieItemObj
    serie_item = SerieItemObj

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
