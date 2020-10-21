from flask import current_app
from sqlalchemy import func, text

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import MovieModel, MetaUserMovieModel, GenreModel, ContentType, UserModel
from src.schemas import MovieBase, MovieObject, GenreBase, MetaUserMovieBase


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
            movie_data = MovieObject.loads(movies)

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
    def get_ordered_genre():
        genres = GenreModel.query.filter_by(
            content_type=ContentType.MOVIE).order_by(GenreModel.count.desc()).all()

        try:
            genres_data = GenreBase.loads(genres)

            resp = message(True, "Movie genres data sent")
            resp["content"] = genres_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_meta(user_uuid, movie_id):
        """ Get specific 'meta_user_movie' data """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            if not (meta_user_movie := MetaUserMovieModel.query.filter_by(user_id=user.user_id, movie_id=movie_id).first()):
                meta_user_movie = MetaUserMovieModel(
                    movie_id=movie_id, user_id=user.user_id, review_see_count=0)

            # Increment meta see
            meta_user_movie.review_see_count += 1
            db.session.add(meta_user_movie)
            db.session.commit()

            meta_user_movie_data = MetaUserMovieBase.load(meta_user_movie)

            resp = message(True, "Meta successfully sent")
            resp["content"] = meta_user_movie_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(user_uuid, movie_id, data):
        """ Updta 'additional_watch_count' or/and update 'rating' """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (movie := MovieModel.query.filter_by(movie_id=movie_id).first()):
            return err_resp("Movie not found!", 404)

        try:
            if not (meta_user_movie := MetaUserMovieModel.query.filter_by(user_id=user.user_id, movie_id=movie_id).first()):
                meta_user_movie = MetaUserMovieModel(
                    movie_id=movie_id, user_id=user.user_id, watch_count=0)

            if 'rating' in data:
                # Update average rating on object
                movie.rating = movie.rating or 0
                movie.rating_count = movie.rating_count or 0
                count = movie.rating_count + \
                    (1 if meta_user_movie.rating is None else 0)
                movie.rating = (movie.rating * movie.rating_count - (
                    meta_user_movie.rating if meta_user_movie.rating is not None else 0) + data["rating"]) / count
                movie.rating_count = count

                meta_user_movie.rating = data["rating"]
            if 'additional_watch_count' in data:
                meta_user_movie.watch_count += data['additional_watch_count']

            db.session.add(meta_user_movie)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
