from flask import current_app
from sqlalchemy import func, text, select
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import MovieModel, MetaUserMovieModel, GenreModel, ContentType, UserModel, RecommendedMovieModel, RecommendedMovieForGroupModel, BadRecommendationMovieModel
from src.schemas import MovieBase, MovieObject, GenreBase, MetaUserMovieBase, MovieExtra


class MovieService:
    @staticmethod
    def search_movie_data(search_term, page, connected_user_uuid):
        """ Search movie data by title """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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
    def get_recommended_movies(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Query for recommendation from user
        for_user_query = db.session.query(RecommendedMovieModel, MovieModel)\
            .select_from(RecommendedMovieModel)\
            .outerjoin(MovieModel, MovieModel.movie_id == RecommendedMovieModel.movie_id)\
            .filter(RecommendedMovieModel.user_id == user.user_id)

        # Query for recommendation from group
        groups_ids = [
            *list(map(lambda x: x.group_id, user.groups)),
            *list(map(lambda x: x.group_id, user.owned_groups))
        ]

        for_group_query = db.session.query(RecommendedMovieForGroupModel, MovieModel)\
            .select_from(RecommendedMovieForGroupModel)\
            .outerjoin(MovieModel, MovieModel.movie_id == RecommendedMovieForGroupModel.movie_id)\
            .filter(RecommendedMovieForGroupModel.group_id.in_(groups_ids))

        # Popularity
        popularity_query = db.session.query(
            func.cast(null(), db.Integer),
            func.cast(null(), db.Integer),
            func.cast(null(), db.Float),
            null(),
            func.cast(null(), db.Integer),
            MovieModel
        ).order_by(
            MovieModel.popularity_score.desc().nullslast(),
        ).limit(200).subquery()

        movies, total_pages = Paginator.get_from(
            for_user_query
            .union(for_group_query)
            .union(select([popularity_query]))
            .order_by(
                RecommendedMovieModel.engine_priority.desc().nullslast(),
                RecommendedMovieModel.score.desc(),
                MovieModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                if row[0] is None:
                    movie = MovieExtra.load(row[1])
                else:
                    movie = MovieExtra.load(row[1])
                    movie["reco_engine"] = row[0].engine
                    movie["reco_score"] = row[0].score
                return movie

            movie_data = list(map(c_load, movies))

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
    def get_ordered_genre(connected_user_uuid):
        if not ( UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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

        if not ( MovieModel.query.filter_by(movie_id=movie_id).first()):
            return err_resp("Application not found!", 404)

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

    @staticmethod
    def add_bad_recommendation(user_uuid, movie_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (movie := MovieModel.query.filter_by(movie_id=movie_id).first()):
            return err_resp("Movie not found!", 404)
        
        try:
            for rc in  data['reason_categorie'].split(','):
                for r in data['reason'].split(','):

                    new_bad_reco = BadRecommendationMovieModel(
                        user_id = user.id,
                        movie_id = movie.movie_id,
                        reason_categorie = rc,
                        reason = r
                    )

                    db.session.add(new_bad_reco)
                    db.session.flush()
            db.session.commit()

            resp = message(True, "Bad recommendation has been registered.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()