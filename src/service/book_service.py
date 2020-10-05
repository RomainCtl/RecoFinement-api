from flask import current_app
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
            db.session.query(BookModel, func.count(
                MetaUserBookModel.user_id).label("count")).join(MetaUserBookModel).group_by(BookModel).order_by(text("count DESC")),
            page,
        )

        try:
            books = map(lambda t: t[0], books)
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