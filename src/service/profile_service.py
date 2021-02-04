from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy.orm import subqueryload
import requests

from src import db
from settings import ENGINE_APIKEY, ENGINE_URL
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import ProfileModel, GenreModel, UserModel
from src.schemas import ProfileBase, ProfileObject, ProfileFullObject, GenreBase


class ProfileService:
    @staticmethod
    def get_profiles(connected_user_uuid):
        """" Get user's profile list """
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        profiles = ProfileModel.query.filter_by(user_id=user.user_id).all()

        try:
            profile_data = ProfileObject.loads(profiles)

            resp = message(True, "Profile data sent")
            resp["profiles"] = profile_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def create_profile(data, connected_user_uuid):
        """ Create new profile """
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        if ProfileModel.query.filter_by(user_id=user.user_id, profilename=data["profilename"]).first() is not None:
            return err_resp("You have already created a profile with this name!", 400)

        try:
            new_profile = ProfileModel(
                profilename=data["profilename"],
                user_id=user.user_id
            )

            db.session.add(new_profile)
            db.session.commit()

            profile_data = ProfileObject.load(new_profile)

            resp = message(True, "Profile created")
            resp["profile"] = profile_data

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_data(uuid, connected_profile_uuid):
        """ Get profile's data by uuid """

        if not (profile := ProfileModel.query.filter_by(uuid=uuid).first()):
            return err_resp("User Profile not found!", 404)

        if not (user := UserModel.query.filter_by(uuid=connected_profile_uuid).first()):
            return err_resp("User not found!", 404)
        if not (ProfileModel.query.filter_by(uuid=uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        try:
            profile_data = ProfileObject.load(profile)

            resp = message(True, "Profile data sent")
            resp["profile"] = profile_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_genres(connected_uuid, uuid_profile):
        """ Get profile liked genre list """
        if not (user := UserModel.query.filter_by(uuid=connected_uuid).first()):
            return err_resp("User not found!", 404)
        if not (profile := ProfileModel.query.filter_by(user_id=user.user_id, uuid=uuid_profile).first()):
            return err_resp("Profile not found!", 404)

        try:
            genres_data = GenreBase.loads(profile.liked_genres)

            resp = message(True, "Profile liked genre sent")
            resp["content"] = genres_data
            return resp, 200
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def like_genre(genre_id, user_uuid, profile_uuid):
        """" Like a genre """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        if not (profile := ProfileModel.query.filter_by(user_id=user.user_id, uuid=profile_uuid).first()):
            return err_resp("Profile not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (genre := GenreModel.query.filter_by(genre_id=genre_id).first()):
            return err_resp("Genre not found!", 404)

        try:
            profile.liked_genres.append(genre)

            db.session.add(profile)
            db.session.commit()

            resp = message(True, "Profile liked this genre")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def unlike_genre(genre_id, user_uuid, profile_uuid):
        """" Unlike a genre """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)
        if not (profile := ProfileModel.query.filter_by(user_id=user.user_id, uuid=profile_uuid).first()):
            return err_resp("Profile not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (genre := GenreModel.query.filter_by(genre_id=genre_id).first()):
            return err_resp("Genre not found!", 404)

        if genre not in profile.liked_genres:
            return err_resp("You didn't like this genre", 400)

        try:
            profile.liked_genres.remove(genre)

            db.session.add(profile)
            db.session.commit()

            resp = message(True, "Profile liked this genre")
            return resp, 201
        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_profile_data(profile_uuid, connected_profile_uuid, data):
        """ Update profile data profilename """

        if not (user := UserModel.query.filter_by(uuid=connected_profile_uuid).first()):
            return err_resp("User not found!", 404)
        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if str(user.uuid) != connected_profile_uuid:
            return err_resp("Unable to update an account which is not your's", 403)

        try:
            if 'profilename' in data.keys():
                profile.profilename = data['profilename']

            db.session.add(profile)
            db.session.commit()

            resp = message(True, "Profile updated successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def delete_account(profile_uuid, connected_profile_uuid):
        """" Delete profile account """

        if not (user := UserModel.query.filter_by(uuid=connected_profile_uuid).first()):
            return err_resp("User not found!", 404)
        if not (ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (ProfileModel.query.filter_by(user_id=user.user_id, uuid=profile_uuid).first()):
            return err_resp("Unable to delete an account which is not your's", 403)

        try:
            ProfileModel.query.filter_by(uuid=profile_uuid).delete()

            db.session.commit()

            resp = message(True, "Profile deleted successfully")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta(profile_uuid, connected_user_uuid):
        """ Get profile meta """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)
