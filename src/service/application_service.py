from settings import REASON_CATEGORIES
from flask import current_app
from sqlalchemy import func, text, select
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import ApplicationModel, UserModel, GenreModel, ContentType, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel
from src.schemas import ApplicationBase, GenreBase, MetaUserContentBase, ApplicationExtra


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
    def get_popular_applications(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # NOTE IMDB measure of popularity does not seem to be relevant for this media.
        applications, total_pages = Paginator.get_from(
            ApplicationModel.query.join(ApplicationModel.content, aliased=True).order_by(
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
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
    def get_recommended_applications_for_user(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        applications, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, ApplicationModel)
            .join(ApplicationModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentModel.user_id == user.user_id)
            .order_by(
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = ApplicationExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

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
    def get_recommended_applications_for_group(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        applications, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, ApplicationModel)
            .join(ApplicationModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(RecommendedContentForGroupModel.group_id.in_(groups_ids))
            .order_by(
                ContentModel.rating_count.desc().nullslast(),
                ContentModel.rating.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = ApplicationExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

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
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
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
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (app := ApplicationModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Application not found!", 404)

        try:
            for rc in data['reason_categorie']:
                if rc in REASON_CATEGORIES['application']:
                    for r in data['reason']:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=app.content_id,
                            reason_categorie=rc,
                            reason=r
                        )

                        db.session.add(new_bad_reco)
                        db.session.flush()
            db.session.commit()

            resp = message(True, "Bad recommendation has been registered.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
