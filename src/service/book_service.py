from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import BookModel, UserModel, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel
from src.schemas import BookBase, BookExtra, MetaUserContentBase


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
    def get_popular_books(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        books, total_pages = Paginator.get_from(
            BookModel.query.join(BookModel.content, aliased=True).order_by(
                ContentModel.popularity_score.desc().nullslast(),
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
    def get_recommended_books_for_user(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        books, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, BookModel)
            .join(BookModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentModel.user_id == user.user_id)
            .order_by(
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
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
    def get_recommended_books_for_group(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        books, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, BookModel)
            .join(BookModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentForGroupModel.group_id.in_(groups_ids))
            .order_by(
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                book = BookExtra.load(row[1])
                book["reco_engine"] = row[0].engine
                book["reco_score"] = row[0].score
                return app

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
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (book := BookModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Book not found!", 404)

        try:
            for type, value in  data.items():
                if type in REASON_CATEGORIES['book'] :
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id = user.user_id,
                            content_id=book.content_id,
                            reason_categorie = type,
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
