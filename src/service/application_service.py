from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import ApplicationModel, UserModel, MetaUserApplicationModel, GenreModel, ContentType
from src.schemas import ApplicationBase, GenreBase, MetaUserApplicationBase


class ApplicationService:
    @staticmethod
    def search_application_data(search_term, page):
        """ Search application data by name """
        applications, total_pages = Paginator.get_from(
            ApplicationModel.query.filter(ApplicationModel.name.ilike(search_term+"%")).union(
                ApplicationModel.query.filter(ApplicationModel.name.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            application_data = ApplicationBase.loads(applications)

            return pagination_resp(
                message="Application data sent",
                content=application_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_applications(page):
        applications, total_pages = Paginator.get_from(
            ApplicationModel.query.filter(ApplicationModel.popularity_score != None).order_by(
                ApplicationModel.popularity_score.desc().nullslast()
            ),
            page,
        )

        try:
            application_data = ApplicationBase.loads(applications)

            return pagination_resp(
                message="Most popular application data sent",
                content=application_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_ordered_genres():
        genres = GenreModel.query.filter_by(
            content_type=ContentType.APPLICATION).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Application genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_meta(user_uuid, app_id):
        """ Get specific 'meta_user_application' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_application := MetaUserApplicationModel.query.filter_by(user_id=user.user_id, app_id=app_id).first()):
                meta_user_application = MetaUserApplicationModel(
                    app_id=app_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_application.review_see_count += 1
            db.session.add(meta_user_application)
            db.session.commit()

            meta_user_application_data = MetaUserApplicationBase.load(
                meta_user_application)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_application_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, app_id, data):
        """ Update 'review' or/and 'downloaded' or/and 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (app := ApplicationModel.query.filter_by(app_id=app_id).first()):
            return err_resp("Application not found!", 404)

        try:
            if not (meta_user_application := MetaUserApplicationModel.query.filter_by(user_id=user.user_id, app_id=app_id).first()):
                meta_user_application = MetaUserApplicationModel(
                    app_id=app_id, user_id=user.user_id)

            if 'rating' in data:
                # Update average rating on object
                app.rating = app.rating or 0
                app.reviews = app.reviews or 0
                count = app.reviews + \
                    (1 if meta_user_application.rating is None else 0)
                app.rating = (app.rating * app.reviews - (
                    meta_user_application.rating if meta_user_application.rating is not None else 0) + data["rating"]) / count
                app.reviews = count

                meta_user_application.rating = data["rating"]
            if 'review' in data:
                meta_user_application.review = data['review']
            if 'downloaded' in data:
                meta_user_application.downloaded = data['downloaded']

            db.session.add(meta_user_application)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
