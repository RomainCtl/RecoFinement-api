from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import BookModel, MetaUserBookModel, UserModel
from src.schemas import BookBase, MetaUserBookBase


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
    def get_meta(user_uuid, isbn):
        """ Get specific 'meta_user_book' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_book := MetaUserBookModel.query.filter_by(user_id=user.user_id, isbn=isbn).first()):
                meta_user_book = MetaUserBookModel(
                    isbn=isbn, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_book.review_see_count += 1
            db.session.add(meta_user_book)
            db.session.commit()

            meta_user_book_data = MetaUserBookBase.load(meta_user_book)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_book_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, isbn, data):
        """ Add 'purchase' or/and update 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (book := BookModel.query.filter_by(isbn=isbn).first()):
            return err_resp("Book not found!", 404)

        try:
            if not (meta_user_book := MetaUserBookModel.query.filter_by(user_id=user.user_id, isbn=isbn).first()):
                meta_user_book = MetaUserBookModel(
                    isbn_isbn, user_id=user.user_id)

            if 'rating' in data:
                # Update average rating on object
                book.rating = book.rating or 0
                book.rating_count = book.rating_count or 0
                count = book.rating_count + \
                    (1 if meta_user_book.rating is None else 0)
                book.rating = (book.rating * book.rating_count - (
                    meta_user_book.rating if meta_user_book.rating is not None else 0) + data["rating"]) / count
                book.rating_count = count

                meta_user_book.rating = data["rating"]
            if 'purchase' in data:
                meta_user_book.purchase = data['purchase']

            db.session.add(meta_user_book)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
