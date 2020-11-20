from flask import current_app
from sqlalchemy import func, text, select, nulls_last
from sqlalchemy.sql.expression import null
from sqlalchemy.sql.elements import Null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import ApplicationModel, UserModel, MetaUserApplicationModel, GenreModel, ContentType, RecommendedApplicationModel, RecommendedApplicationForGroupModel
from src.schemas import ApplicationBase, GenreBase, MetaUserApplicationBase, ApplicationExtra


class ApplicationService:
    @staticmethod
    def search_application_data(search_term, page, connected_user_uuid):
        """ Search application data by name """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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
    def get_recommended_applications(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from user
        for_user_query = db.session.query(RecommendedApplicationModel, ApplicationModel)\
            .select_from(RecommendedApplicationModel)\
            .outerjoin(ApplicationModel, ApplicationModel.app_id == RecommendedApplicationModel.app_id)\
            .filter(RecommendedApplicationModel.user_id == user.user_id)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        for_group_query = db.session.query(RecommendedApplicationForGroupModel, ApplicationModel)\
            .select_from(RecommendedApplicationForGroupModel)\
            .outerjoin(ApplicationModel, ApplicationModel.app_id == RecommendedApplicationForGroupModel.app_id)\
            .filter(RecommendedApplicationForGroupModel.group_id.in_(groups_ids))

        # NOTE IMDB measure of popularity does not seem to be relevant for this media.
        popularity_query = db.session.query(
            func.cast(null(), db.Integer),
            func.cast(null(), db.Integer),
            func.cast(null(), db.Float),
            null(),
            func.cast(null(), db.Integer),
            ApplicationModel
        ).order_by(
            nulls_last(ApplicationModel.reviews.desc().nullslast(),
            nulls_last(ApplicationModel.rating.desc().nullslast(),
        ).limit(200).subquery()

        applications, total_pages = Paginator.get_from(
            for_user_query
            .union(for_group_query)
            .union(select([popularity_query]))
            .order_by(
                RecommendedApplicationModel.engine_priority.desc().nullslast(),
                RecommendedApplicationModel.score.desc().nullslast(),
                ApplicationModel.reviews.desc().nullslast(),
                ApplicationModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                if row[0] is None:
                    game = ApplicationExtra.load(row[1])
                else:
                    game = ApplicationExtra.load(row[1])
                    game["reco_engine"] = row[0].engine
                    game["reco_score"] = row[0].score
                return game

            application_data = list(map(c_load, applications))

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
    def get_ordered_genres(connected_user_uuid):
        if not ( UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
        
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

        if not ( ApplicationModel.query.filter_by(app_id=app_id).first()):
            return err_resp("Application not found!", 404)

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
