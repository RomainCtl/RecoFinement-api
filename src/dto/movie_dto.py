from flask_restx import Namespace, fields

from .base import MovieBaseObj, paginationObj, GenreBaseObj, messageObj


class MovieDto:
    api = Namespace("movie", description="Movie related operations.")

    # Objects
    api.models[MovieBaseObj.name] = MovieBaseObj
    movie_base = MovieBaseObj

    api.models[GenreBaseObj.name] = GenreBaseObj
    genre_base = GenreBaseObj

    # Responses
    data_resp = api.clone(
        "Movie list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(movie_base)),
        },
    )

    genres_resp = api.clone(
        "Movie genres Data Response",
        messageObj,
        {
            "content": fields.List(fields.Nested(genre_base))
        }
    )

    # Excepted data
    movie_meta = api.model(
        "MovieMetaExpected",
        {
            "additional_watch_count": fields.Integer(min=1),
            "rating": fields.Integer(min=0, max=5),
        }
    )
