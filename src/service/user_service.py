from flask import current_app

from src import db
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import UserModel, ApplicationModel, BookModel, GameModel, MovieModel, SerieModel, TrackModel, MetaUserApplicationModel, MetaUserBookModel, MetaUserGameModel, MetaUserMovieModel, MetaUserSerieModel, MetaUserTrackModel
from src.schemas import UserBase, UserObject


class UserService:
    @staticmethod
    def search_user_data(search_term, page):
        """ Search user data by username """
        users, total_pages = Paginator.get_from(
            UserModel.query.filter(UserModel.username.ilike(search_term+"%")).union(
                UserModel.query.filter(UserModel.username.ilike("%"+search_term+"%"))),
            page,
        )

        try:
            user_data = UserBase.loads(users)

            return pagination_resp(
                message="Track data sent",
                content=user_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_user_data(uuid):
        """ Get user's data by uuid """
        if not (user := UserModel.query.filter_by(uuid=uuid).first()):
            return err_resp("User not found!", 404)

        try:
            user_data = UserObject.load(user)

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_application(app_id, rating, user_uuid):
        """" Give rate to an application """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not ApplicationModel.query.filter_by(app_id=app_id).first():
            return err_resp("Application not found!", 404)

        try:
            meta_user_application = MetaUserApplicationModel(
                app_id=app_id, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_application)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_book(isbn, rating, user_uuid):
        """" Give rate to a book """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not BookModel.query.filter_by(isbn=isbn).first():
            return err_resp("Book not found!", 404)

        try:
            meta_user_book = MetaUserBookModel(
                isbn=isbn, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_book)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_game(game_id, rating, user_uuid):
        """" Give rate to a game """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not GameModel.query.filter_by(game_id=game_id).first():
            return err_resp("Game not found!", 404)

        try:
            meta_user_game = MetaUserGameModel(
                game_id=game_id, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_game)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_movie(movie_id, rating, user_uuid):
        """" Give rate to a movie """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not MovieModel.query.filter_by(movie_id=movie_id).first():
            return err_resp("Movie not found!", 404)

        try:
            meta_user_movie = MetaUserMovieModel(
                movie_id=movie_id, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_movie)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_serie(serie_id, rating, user_uuid):
        """" Give rate to a serie """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not SerieModel.query.filter_by(serie_id=serie_id).first():
            return err_resp("Serie not found!", 404)

        try:
            meta_user_serie = MetaUserSerieModel(
                serie_id=serie_id, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_serie)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def rate_track(track_id, rating, user_uuid):
        """" Give rate to a track """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not TrackModel.query.filter_by(track_id=track_id).first():
            return err_resp("Track not found!", 404)

        try:
            meta_user_track = MetaUserTrackModel(
                track_id=track_id, user_id=user.user_id, rating=rating)

            db.session.add(meta_user_track)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
