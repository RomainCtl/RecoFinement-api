from settings import REASON_CATEGORIES
from flask import current_app
from sqlalchemy import func, text, select
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import BookModel, MetaUserBookModel, UserModel, RecommendedBookModel, RecommendedBookForGroupModel, BadRecommendationBookModel
from src.schemas import BookBase, MetaUserBookBase, BookExtra


class BookService:
    @staticmethod
    def search_book_data(search_term, page, connected_user_uuid):
        """ Search book data by title """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
                return err_resp("User not found!", 404)
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
        
        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "view_recommendation" not in permissions :
            return err_resp("Permission missing", 403)

        # Query for recommendation from user
        for_user_query = db.session.query(RecommendedBookModel, BookModel)\
            .select_from(RecommendedBookModel)\
            .outerjoin(BookModel, BookModel.isbn == RecommendedBookModel.isbn)\
            .filter(RecommendedBookModel.user_id == user.user_id)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        for_group_query = db.session.query(RecommendedBookForGroupModel, BookModel)\
            .select_from(RecommendedBookForGroupModel)\
            .outerjoin(BookModel, BookModel.isbn == RecommendedBookForGroupModel.isbn)\
            .filter(RecommendedBookForGroupModel.group_id.in_(groups_ids))

        # Popularity
        popularity_query = db.session.query(
            func.cast(null(), db.Integer),
            null(),
            func.cast(null(), db.Float),
            null(),
            func.cast(null(), db.Integer),
            BookModel
        ).order_by(
            BookModel.popularity_score.desc().nullslast(),
        ).limit(200).subquery()

        books, total_pages = Paginator.get_from(
            for_user_query
            .union(for_group_query)
            .union(select([popularity_query]))
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
        if not (BookModel.query.filter_by(isbn=isbn).first()):
            return err_resp("Book not found!", 404)

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

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "indicate_interest" not in permissions :
            return err_resp("Permission missing", 403)

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


    @staticmethod
    def add_bad_recommendation(user_uuid, isbn, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "indicate_interest" not in permissions :
            return err_resp("Permission missing", 403)

        if not (book := BookModel.query.filter_by(isbn=isbn).first()):
            return err_resp("Book not found!", 404)
        
        try:
            for rc in  data['reason_categorie']:
                if rc in REASON_CATEGORIES['book'] :
                    for r in data['reason']:

                        new_bad_reco = BadRecommendationBookModel(
                            user_id = user.id,
                            isbn = book.isbn,
                            reason_categorie = rc,
                            reason = r
                        )

                        db.session.add(new_bad_reco)
                        db.session.flush()
            db.session.commit()

            resp = message(True, "Bad recommendation has been registered.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()