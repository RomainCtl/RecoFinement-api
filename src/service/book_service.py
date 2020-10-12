from flask import current_app, jsonify
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import BookModel, MetaUserBookModel
from src.schemas import BookBase


class BookService:
    @staticmethod
    def search_book_data(search_term, page):
        """ Search book data by title """
        books, total_pages = Paginator.get_from(
            BookModel.query.filter(BookModel.title.ilike(search_term+"%")).union(
                BookModel.query.filter(BookModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            book_data = BookBase.loads(books)

            return pagination_resp(
                message="Book data sent",
                content=book_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_books(page):
        books, total_pages = Paginator.get_from(
            BookModel.query.order_by(
                BookModel.rating_count.desc().nullslast(),
                BookModel.rating.desc().nullslast()
            ),
            page,
        )

        try:
            book_data = BookBase.loads(books)

            return pagination_resp(
                message="Most popular book data sent",
                content=book_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_book_data(id):
        """ Get book data by id """
        book = BookModel.query.filter(BookModel.isbn==id)
        try:
            book_data = BookBase.loads(book)

            return jsonify(
                message="Book data sent",
                content=book_data
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()