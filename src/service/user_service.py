from flask import current_app

from src import db
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import UserModel, ApplicationModel, BookModel, GameModel, MovieModel, SerieModel, TrackModel, MetaUserApplicationModel, MetaUserBookModel, MetaUserGameModel, MetaUserMovieModel, MetaUserSerieModel, MetaUserTrackModel, GenreModel
from src.schemas import UserBase, UserObject, GenreBase


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
    def rate_serie(serie_id, rating, user_uuid):
        """" Give rate to a serie """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (serie := SerieModel.query.filter_by(serie_id=serie_id).first()):
            return err_resp("Serie not found!", 404)

        try:
            meta_user_serie = MetaUserSerieModel(
                serie_id=serie_id, user_id=user.user_id, rating=rating)

            # Update average rating on object
            serie.rating = serie.rating or 0
            serie.rating_count = serie.rating_count or 0
            serie.rating = (serie.rating * serie.rating_count +
                            rating) / (serie.rating_count + 1)
            serie.rating_count += 1

            db.session.add(meta_user_serie)
            db.session.commit()

            resp = message(True, "Rating given successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_genres(user_uuid):
        """ Get user liked genre list """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        try:
            genres_data = GenreBase.loads(user.liked_genres)

            resp = message(True, "User liked genre sent")
            resp["content"] = genres_data
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def like_genre(genre_id, user_uuid):
        """" Like a genre """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (genre := GenreModel.query.filter_by(genre_id=genre_id).first()):
            return err_resp("Genre not found!", 404)

        try:
            user.liked_genres.append(genre)

            db.session.add(user)
            db.session.commit()

            resp = message(True, "User liked this genre")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def unlike_genre(genre_id, user_uuid):
        """" Unlike a genre """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (genre := GenreModel.query.filter_by(genre_id=genre_id).first()):
            return err_resp("Genre not found!", 404)

        if genre not in user.liked_genres:
            return err_resp("You didn't like this genre", 400)

        try:
            user.liked_genres.remove(genre)

            db.session.add(user)
            db.session.commit()

            resp = message(True, "User liked this genre")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
