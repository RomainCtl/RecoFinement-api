from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import SerieModel, MetaUserSerieModel
from src.schemas import SerieBase


class SerieService:
    @staticmethod
    def search_serie_data(search_term, page):
        """ Search serie data by title """
        series, total_pages = Paginator.get_from(
            SerieModel.query.filter(SerieModel.title.ilike(search_term+"%")).union(
                SerieModel.query.filter(SerieModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            serie_data = SerieBase.loads(series)

            return pagination_resp(
                message="Serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_series(page):
        series, total_pages = Paginator.get_from(
            db.session.query(SerieModel, func.count(
                MetaUserSerieModel.user_id).label("count")).outerjoin(MetaUserSerieModel).group_by(SerieModel.serie_id).order_by(text("count DESC")),
            page,
        )

        try:
            series = map(lambda t: t[0], series)
            serie_data = SerieBase.loads(series)

            return pagination_resp(
                message="Most popular serie data sent",
                content=serie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
