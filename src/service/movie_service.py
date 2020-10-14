from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator
from src.model import MovieModel, MetaUserMovieModel, GenreModel, ContentType
from src.schemas import MovieBase, GenreBase


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
            MovieModel.query.order_by(
                MovieModel.rating_count.desc().nullslast(),
                MovieModel.rating.desc().nullslast()
            ),
            page,
        )

        try:
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

    @staticmethod
    def get_ordered_genre(self):
        genres = GenreModel.query.filter_by(
            content_type=ContentType.MOVIE).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Movie genres data sent")
            resp["movie_genres"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
