from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select, and_
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import ApplicationModel, UserModel, GenreModel, ContentType, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel, ApplicationAdditionalModel
from src.schemas import ApplicationBase, GenreBase, MetaUserContentBase, ApplicationExtra, ApplicationAdditionalBase


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
    def get_recommended_applications_for_user(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        filters = [RecommendedContentModel.user_id == user.user_id]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        applications, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, ApplicationModel)
            .join(ApplicationModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
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
    def get_recommended_applications_for_group(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        filters = [RecommendedContentForGroupModel.group_id.in_(groups_ids)]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        applications, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, ApplicationModel)
            .join(ApplicationModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
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

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "indicate_interest" not in permissions:
            return err_resp("Permission missing", 403)

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
            for type, value in data.items():
                if type in REASON_CATEGORIES['application']:
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=app.content_id,
                            reason_categorie=type,
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

    @staticmethod
    def add_additional_application(user_uuid, data):
        """ Add additional application"""
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        try:

            new_additional_application = ApplicationAdditionalModel(
                name=data['name'],
            )

            if 'size' in data:
                new_additional_application.size = data['size']
            if 'installs' in data:
                new_additional_application.installs = data['installs']
            if 'type' in data:
                new_additional_application.type = data['type']
            if 'price' in data:
                new_additional_application.price = data['price']
            if 'content_rating' in data:
                new_additional_application.content_rating = data['content_rating']
            if 'last_updated' in data:
                new_additional_application.last_updated = data['last_updated']
            if 'current_version' in data:
                new_additional_application.current_version = data['current_version']
            if 'android_version' in data:
                new_additional_application.android_version = data['android_version']
            if 'cover' in data:
                new_additional_application.cover = data['cover']

            for genre_id in data["genres"]:
                if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                    new_additional_application.genres.append(ge)
                else:
                    return err_resp("Genre %s not found!" % genre_id, 404)

            db.session.add(new_additional_application)
            db.session.commit()

            resp = message(True, "Application have been added to validation.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_additional_application(connected_user_uuid, page):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        applications, total_pages = Paginator.get_from(
            ApplicationAdditionalModel.query,
            page,
        )

        try:
            application_data = ApplicationAdditionalBase.loads(applications)

            return pagination_resp(
                message="Additional application data sent",
                content=application_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def validate_additional_application(connected_user_uuid, app_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "validate_added_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (app := ApplicationAdditionalModel.query.filter_by(app_id=app_id).first()):
            return err_resp("Additional application not found!", 404)

        try:
            content = ContentModel(rating=None, genres=app.genres)
            db.session.add(content)
            db.session.flush()

            new_application = ApplicationModel(
                name=app.name,
                size=app.size,
                installs=app.installs,
                type=app.type,
                price=app.price,
                content_rating=app.content_rating,
                last_updated=app.last_updated,
                current_version=app.current_version,
                android_version=app.android_version,
                cover=app.cover,
                content=content
            )
            db.session.add(new_application)
            db.session.delete(app)

            db.session.commit()

            resp = message(
                True, "Additional application data successfully validated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def decline_additional_application(connected_user_uuid, app_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "delete_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (app := ApplicationAdditionalModel.query.filter_by(app_id=app_id).first()):
            return err_resp("Additional application not found!", 404)

        try:
            db.session.delete(app)
            db.session.commit()

            resp = message(True, "Additional application successfully deleted")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
