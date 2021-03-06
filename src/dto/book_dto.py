from flask_restx import Namespace, fields

from .base import BookBaseObj, messageObj, paginationObj, BookAdditionalBaseObj


class BookDto:
    api = Namespace("book", description="Book related operations.")

    # Objects
    api.models[BookBaseObj.name] = BookBaseObj
    book_base = BookBaseObj

    api.models[BookAdditionalBaseObj.name] = BookAdditionalBaseObj
    book_additional_base = BookAdditionalBaseObj

    # Responses
    data_resp = api.clone(
        "Book list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(book_base)),
        },
    )

    # Excepted data
    book_meta = api.model(
        "BookMetaExpected",
        {
            "purchase": fields.Boolean,
            "rating": fields.Integer(min=0, max=5),
        }
    )

    book_bad_recommendation = api.model(
        "BookBadRecommendationMetaExpected",
        {
            "author": fields.List(fields.String),
            "publisher": fields.List(fields.String),
            "year_of_publication": fields.List(fields.String)
        }
    )
