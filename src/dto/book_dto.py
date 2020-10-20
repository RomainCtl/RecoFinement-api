from flask_restx import Namespace, fields

from .base import BookBaseObj, messageObj, paginationObj, MetaUserBookBaseObj


class BookDto:
    api = Namespace("book", description="Book related operations.")

    # Objects
    api.models[BookBaseObj.name] = BookBaseObj
    book_base = BookBaseObj

    api.models[MetaUserBookBaseObj.name] = MetaUserBookBaseObj
    meta_user_book_base = MetaUserBookBaseObj

    # Responses
    data_resp = api.clone(
        "Book list Data Response",
        paginationObj,
        {
            "content": fields.List(fields.Nested(book_base)),
        },
    )

    meta_resp = api.clone(
        "MetaUserBook Data Response",
        messageObj,
        {
            "content": fields.Nested(meta_user_book_base)
        }
    )

    # Excepted data
    book_meta = api.model(
        "BookMetaExpected",
        {
            "purchase": fields.Boolean,
            "rating": fields.Integer(min=0, max=5),
        }
    )
