from flask_restx import Namespace, fields

from .base import SerieBaseObj, SerieItemObj, paginationObj, messageObj, GenreBaseObj, MetaUserSerieBaseObj


class SerieDto:
    api = Namespace("serie", description="Serie related operations.")

    # Objects
    api.models[SerieBaseObj.name] = SerieBaseObj
    serie_base = SerieBaseObj

    api.models[SerieItemObj.name] = SerieItemObj
    serie_item = SerieItemObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    api.models[MetaUserSerieBaseObj.name] = MetaUserSerieBaseObj
    meta_user_serie_base = MetaUserSerieBaseObj

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

    meta_resp = api.clone(
        "MetaUserSerie Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_user_serie_base)
        }
    )

    # Excepted data
    serie_meta = api.model(
        "SeireMetaExpected",
        {
            "num_watched_episodes": fields.Integer(min=1),
            "rating": fields.Integer(min=0, max=5),
        }
    )
