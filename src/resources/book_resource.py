from flask import request
from flask_restx import Resource
from flask_jwt_extended import jwt_required

from src.service import BookService
from src.dto import BookDto

api = BookDto.api
data_resp = BookDto.data_resp


@api.route("", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookResource(Resource):
    @api.doc(
        "Get list of the most popular Books",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self):
        """ Get list of the most popular Books """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return BookService.get_most_popular_books(page)


@api.route("/search/<string:search_term>", doc={"params": {"page": {"in": "query", "type": "int", "default": 1}}})
class BookSearchResource(Resource):
    @api.doc(
        "Search books",
        responses={
            200: ("Book data successfully sent", data_resp),
            401: ("Authentication required"),
        },
    )
    @jwt_required
    def get(self, search_term):
        """ Getlist of book's data by term """
        try:
            page = int(request.args.get('page'))
        except ValueError:
            page = 1
        return BookService.search_book_data(search_term, page)

    @api.route("/<string:bookID>")
    class BookSearchResource(Resource):
        @api.doc(
            "Get book",
            responses={
                200: ("Book data successfully sent", data_resp),
                401: ("Authentication required"),
            },
        )
        @jwt_required
        def get(self, bookID):
            """ Getlist of book's data by term """
            return BookService.get_book_data(bookID)