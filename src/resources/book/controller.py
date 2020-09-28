from flask_restx import Resource
from flask_jwt_extended import jwt_required

from .service import BookService
from .dto import BookDto

api = BookDto.api
data_resp = BookDto.data_resp


@api.route("/<string:isbn>")
class BookController(Resource):
    @api.doc(
        "Get a specific book",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
            404: "Book not found!",
        },
    )
    @jwt_required
    def get(self, isbn):
        """ Get a specific book's data by their isbn """
        return BookService.get_book_data(isbn)
