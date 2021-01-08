from flask_restx import Namespace, fields

from .base import BookBaseObj, messageObj, paginationObj


class BookDto:
    api = Namespace("book", description="Book related operations.")

    # Objects
    api.models[BookBaseObj.name] = BookBaseObj
    book_base = BookBaseObj

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
