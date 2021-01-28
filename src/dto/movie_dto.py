from flask_restx import Namespace, fields

from .base import MovieBaseObj, paginationObj, messageObj, MovieAdditionalBaseObj


class MovieDto:
    api = Namespace("movie", description="Movie related operations.")

    # Objects
    api.models[MovieBaseObj.name] = MovieBaseObj
    movie_base = MovieBaseObj

    api.models[MovieAdditionalBaseObj.name] = MovieAdditionalBaseObj
    movie_additional_base = MovieAdditionalBaseObj

    # Responses
    data_resp = api.clone(
        "Movie list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(movie_base)),
        },
    )

    # Excepted data
    movie_meta = api.model(
        "MovieMetaExpected",
        {
            "additional_watch_count": fields.Integer(min=1),
            "rating": fields.Integer(min=0, max=5),
        }
    )

    movie_bad_recommendation = api.model(
        "MovieBadRecommendationMetaExpected",
        {
            "year": fields.List(fields.String),
            "producers": fields.List(fields.String),
            "genres": fields.List(fields.String),
            "director": fields.List(fields.String),
            "writer": fields.List(fields.String),
            "actors": fields.List(fields.String)
        }
    )
