from settings import REASON_CATEGORIES
from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy import func, text, select, and_
from sqlalchemy.sql.expression import null

from src import db, settings
from src.utils import pagination_resp, internal_err_resp, message, Paginator, err_resp
from src.model import MovieModel, GenreModel, ContentType, UserModel, ContentModel, RecommendedContentModel, RecommendedContentForGroupModel, MetaUserContentModel, BadRecommendationContentModel, MovieAdditionalModel
from src.schemas import MovieBase, MovieObject, GenreBase, MovieExtra, MetaUserContentBase, MovieAdditionalBase


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
    def get_popular_movies(page, connected_user_uuid):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        movie, total_pages = Paginator.get_from(
            MovieModel.query.join(MovieModel.content, aliased=True).order_by(
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            movie_data = MovieObject.loads(movie)

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
    def get_recommended_movies_for_user(page, connected_user_uuid, reco_engine):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        filters = [RecommendedContentModel.user_id == user.user_id]
        if reco_engine is not None:
            filters.append(RecommendedContentModel.engine == reco_engine)

        movies, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentModel, MovieModel)
            .join(MovieModel.content)
            .join(RecommendedContentModel, RecommendedContentModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = MovieExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

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
    def get_recommended_movies_for_group(page, connected_user_uuid, reco_engine):
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

        movies, total_pages = Paginator.get_from(
            db.session.query(RecommendedContentForGroupModel, MovieModel)
            .join(MovieModel.content)
            .join(RecommendedContentForGroupModel, RecommendedContentForGroupModel.content_id == ContentModel.content_id)
            .filter(
                and_(*filters)
            )
            .order_by(
                RecommendedContentModel.score.desc().nullslast(),
                ContentModel.popularity_score.desc().nullslast(),
            ),
            page,
        )

        try:
            def c_load(row):
                app = MovieExtra.load(row[1])
                app["reco_engine"] = row[0].engine
                app["reco_score"] = row[0].score
                return app

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
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
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
    def add_bad_recommendation(user_uuid, content_id, data):
        """ Add bad user recommendation """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (movie := MovieModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Movie not found!", 404)

        try:
            for type, value in data.items():
                if type in REASON_CATEGORIES['movie']:
                    for r in value:

                        new_bad_reco = BadRecommendationContentModel(
                            user_id=user.user_id,
                            content_id=movie.content_id,
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
    def add_additional_movie(user_uuid, data):
        """ Add additional movie"""
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        try:

            new_additional_movie = MovieAdditionalModel(
                title=data['title'],
            )

            if 'language' in data:
                new_additional_movie.language = data['language']
            if 'actors' in data:
                new_additional_movie.actors = data['actors']
            if 'year' in data:
                new_additional_movie.year = data['year']
            if 'producers' in data:
                new_additional_movie.producers = data['producers']
            if 'director' in data:
                new_additional_movie.director = data['director']
            if 'writer' in data:
                new_additional_movie.writer = data['writer']
            if 'imdbid' in data:
                new_additional_movie.imdbid = data['imdbid']
            if 'tmdbid' in data:
                new_additional_movie.tmdbid = data['tmdbid']
            if 'cover' in data:
                new_additional_movie.cover = data['cover']
            if 'plot_outline' in data:
                new_additional_movie.plot_outline = data['plot_outline']

            for genre_id in data["genres"]:
                if (ge := GenreModel.query.filter_by(genre_id=genre_id).first()):
                    new_additional_movie.genres.append(ge)
                else:
                    return err_resp("Genre %s not found!" % genre_id, 404)

            db.session.add(new_additional_movie)
            db.session.commit()

            resp = message(True, "Movie have been added to validation.")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()


    @staticmethod
    def get_additional_movie(connected_user_uuid, page):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "add_content" not in permissions:
            return err_resp("Permission missing", 403)

        movies, total_pages = Paginator.get_from(
            MovieAdditionalModel.query,
            page,
        )

        try:
            movie_data = MovieAdditionalBase.loads(movies)

            return pagination_resp(
                message="Additional movie data sent",
                content=movie_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def validate_additional_movie(connected_user_uuid, movie_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "validate_added_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (movie := MovieAdditionalModel.query.filter_by(movie_id=movie_id).first()):
            return err_resp("Additional movie not found!", 404)

        try:
            content = ContentModel(rating=None, genres=movie.genres)
            db.session.add(content)
            db.session.flush()

            new_movie = MovieModel(
                title=movie.title,
                language=movie.language,
                actors=movie.actors,
                year=movie.year,
                producers=movie.producers,
                director=movie.director,
                writer=movie.writer,
                imdbid=movie.imdbid,
                tmdbid=movie.tmdbid,
                cover=movie.cover,
                plot_outline=movie.plot_outline,
                content=content
            )
            db.session.add(new_movie)
            db.session.delete(movie)

            db.session.commit()

            resp = message(
                True, "Additional movie data successfully validated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def decline_additional_movie(connected_user_uuid, movie_id):
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "delete_content" not in permissions:
            return err_resp("Permission missing", 403)

        if not (movie := MovieAdditionalModel.query.filter_by(movie_id=movie_id).first()):
            return err_resp("Additional movie not found!", 404)

        try:
            db.session.delete(movie)
            db.session.commit()

            resp = message(True, "Additional movie successfully deleted")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()