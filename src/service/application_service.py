from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import ApplicationModel, MetaUserApplicationModel
from src.schemas import ApplicationBase


class ApplicationService:
    @staticmethod
    def search_application_data(search_term, page):
        """ Search application data by title """
        applications, total_pages = Paginator.get_from(
            ApplicationModel.query.filter(ApplicationModel.title.ilike(search_term+"%")).union(
                ApplicationModel.query.filter(ApplicationModel.title.ilike("%"+search_term+"%"))),
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
            db.session.query(ApplicationModel, func.count(
                MetaUserApplicationModel.user_id).label("count")).join(MetaUserApplicationModel).group_by(ApplicationModel).order_by(text("count DESC")),
            page,
        )

        try:
            applications = map(lambda t: t[0], applications)
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
