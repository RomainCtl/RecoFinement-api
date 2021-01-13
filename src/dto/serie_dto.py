from flask_restx import Namespace, fields

from .base import SerieBaseObj, SerieItemObj, paginationObj, messageObj, EpisodeBaseObj


class SerieDto:
    api = Namespace("serie", description="Serie related operations.")

    # Objects
    api.models[SerieBaseObj.name] = SerieBaseObj
    serie_base = SerieBaseObj

    api.models[SerieItemObj.name] = SerieItemObj
    serie_item = SerieItemObj

    api.models[EpisodeBaseObj.name] = EpisodeBaseObj
    episode_base = EpisodeBaseObj

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

    episodes_resp = api.clone(
        "Serie episodes Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(episode_base))
        }
    )

    serie_bad_recommendation = api.model(
        "SerieBadRecommendationMetaExpected",
        {
            "directors": fields.List(fields.String),
            "writers": fields.List(fields.String),
            "start_year": fields.List(fields.String),
            "end_year": fields.List(fields.String),
            "genres": fields.List(fields.String),
            "actors": fields.List(fields.String)
        }
    )
