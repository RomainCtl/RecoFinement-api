from flask_restx import Namespace, fields

from .base import MovieBaseObj, paginationObj


class MovieDto:
    api = Namespace("movie", description="Movie related operations.")

    # Objects
    api.models[MovieBaseObj.name] = MovieBaseObj
    movie_base = MovieBaseObj

    # Responses
    data_resp = api.clone(
        "Movie list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(movie_base)),
        },
    )
