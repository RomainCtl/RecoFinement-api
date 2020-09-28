from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model import Book


class BookService:
    @staticmethod
    def get_book_data(isbn):
        """ Get book data by isbn """
        if not (book := Book.query.filter_by(isbn=isbn).first()):
            return err_resp("Application not found!", 404)

        from .utils import load_data

        try:
            book_data = load_data(book)

            resp = message(True, "Book data sent")
            resp["book"] = book_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
