from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import MovieModel, MetaUserMovieModel
from src.schemas import MovieBase


class MovieService:
    @staticmethod
    def search_movie_data(search_term, page):
        """ Search movie data by title """
        movies, total_pages = Paginator.get_from(
            MovieModel.query.filter(MovieModel.title.ilike(search_term+"%")).union(
                MovieModel.query.filter(MovieModel.title.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            movie_data = MovieBase.loads(movies)

            return pagination_resp(
                message="Movie data sent",
                content=movie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_most_popular_movies(page):
        movies, total_pages = Paginator.get_from(
            db.session.query(MovieModel, func.count(
                MetaUserMovieModel.user_id).label("count")).outerjoin(MetaUserMovieModel).group_by(MovieModel.movie_id).order_by(text("count DESC")),
            page,
        )

        try:
            movies = map(lambda t: t[0], movies)
            movie_data = MovieBase.loads(movies)

            return pagination_resp(
                message="Most popular movie data sent",
                content=movie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
