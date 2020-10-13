from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import SerieModel, MetaUserSerieModel, SSerieGenresModel
from src.schemas import SerieBase, SSerieGenresBase


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
            SerieModel.query.order_by(
                SerieModel.rating_count.desc().nullslast(),
                SerieModel.rating.desc().nullslast()
            ),
            page,
        )

        try:
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

    @staticmethod
    def get_ordered_genre():
        genres = SSerieGenresModel.query.order_by(
            SSerieGenresModel.count.desc()).all()

        try:
            genres_data = SSerieGenresBase.loads(genres)

            resp = message(True, "Serie genres data sent")
            resp["serie_genres"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
