from flask_restx import Namespace, fields

class ApplicationDto:
    api = Namespace("book", description="Book related operations.")
    book = api.model(
        "Book object",
        {
            "isbn": fields.String,
            "title": fields.String,
            "author": fields.String,
            "year_of_publication": fields.Integer,
            "publisher": fields.String,
            "image_url_s": fields.String,
            "image_url_m": fields.String,
            "image_url_l": fields.String,
            "rating": fields.Float,
            "rating_count": fields.Integer,
        },
    )

    data_resp = api.model(
        "Book Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "book": fields.Nested(book),
        },
    )
