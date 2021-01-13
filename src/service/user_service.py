from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy.orm import subqueryload
import requests

from src import db
from settings import ENGINE_APIKEY, ENGINE_URL
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import UserModel, GenreModel
from src.schemas import UserBase, UserObject, UserFullObject, GenreBase


class UserService:
    @staticmethod
    def search_user_data(search_term, page, connected_user_uuid):
        """ Search user data by username """
        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)
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
    def get_user_data(uuid, connected_user_uuid):
        """ Get user's data by uuid """
        if not (user := UserModel.query.filter_by(uuid=uuid).first()):
            return err_resp("User not found!", 404)

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
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
    def export_all_user_data(uuid):
        """ Get user's data by uuid """
        if not (user := UserModel.query.filter_by(uuid=uuid).first()):
            return err_resp("User not found!", 404)

        try:
            user_data = UserFullObject.load(user)

            resp = message(True, "User data exported")
            resp["user"] = user_data
            return resp, 200

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
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def like_genre(genre_id, user_uuid):
        """" Like a genre """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "modify_user_profil" not in permissions:
            return err_resp("Permission missing", 403)

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

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "modify_user_profil" not in permissions:
            return err_resp("Permission missing", 403)

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

    @staticmethod
    def update_user_data(user_uuid, connected_user_uuid, data):
        """ Update user data username - email - password """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "modify_user_profil" not in permissions:
            return err_resp("Permission missing", 403)

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        if str(user_uuid) != connected_user_uuid:
            return err_resp("Unable to update an account which is not your's", 403)

        try:
            if 'username' in data.keys():
                user.username = data['username']
            if 'password' in data.keys():
                user.password = data['password']
            if 'email' in data.keys():
                user.email = data['email']

            db.session.add(user)
            db.session.commit()

            resp = message(True, "User updated successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def set_preferences_defined(connected_user_uuid):
        """  """
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "modify_user_profil" not in permissions:
            return err_resp("Permission missing", 403)

        try:
            user.preferences_defined = True

            db.session.add(user)
            db.session.commit()

            # Send request to reco_engine
            requests.put('%s/recommend/%s' % (ENGINE_URL, user.uuid),
                         headers={'X-API-TOKEN': ENGINE_APIKEY})

            resp = message(True, "User updated successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def delete_account(user_uuid, connected_user_uuid):
        """" Delete user account """
        if not (UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "modify_user_profil" not in permissions:
            return err_resp("Permission missing", 403)

        if not (UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        if str(user_uuid) != str(connected_user_uuid):
            return err_resp("Unable to delete an account which is not your's", 403)

        try:
            UserModel.query.filter_by(uuid=user_uuid).delete()

            db.session.commit()

            resp = message(True, "User account deleted successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
