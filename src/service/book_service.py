from flask import current_app
from sqlalchemy import func, text
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import BookModel, MetaUserBookModel, UserModel, RecommendedBookModel
from src.schemas import BookBase, MetaUserBookBase, BookExtra


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
    def get_recommended_books(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        popularity_query = db.session.query(
            null().label("user_id"),
            null().label("isbn"),
            null().label("score"),
            null().label("engine"),
            null().label("engine_priority"),
            BookModel
        ).order_by(
            BookModel.popularity_score.desc().nullslast(),
        ).limit(200)

        books, total_pages = Paginator.get_from(
            db.session.query(RecommendedBookModel, BookModel)
            .select_from(RecommendedBookModel)
            .outerjoin(BookModel, BookModel.isbn == RecommendedBookModel.isbn)
            .filter(RecommendedBookModel.user_id == user.user_id)
            .union(popularity_query)
            .order_by(
                RecommendedBookModel.engine_priority.desc().nullslast(),
                RecommendedBookModel.score.desc(),
                BookModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                if row[0] is None:
                    book = BookExtra.load(row[1])
                else:
                    book = BookExtra.load(row[1])
                    book["reco_engine"] = row[0].engine
                    book["reco_score"] = row[0].score
                return book

            book_data = list(map(c_load, books))

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
                    isbn, user_id=user.user_id)

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
