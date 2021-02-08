from flask import current_app
from flask_jwt_extended import get_jwt_claims
from sqlalchemy.orm import subqueryload
import requests

from src import db
from settings import ENGINE_APIKEY, ENGINE_URL
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import ProfileModel, GenreModel, UserModel, MetaProfileContentModel, ContentModel, ApplicationModel, BookModel, GameModel, MovieModel, SerieModel, TrackModel
from src.schemas import ProfileBase, ProfileObject, GenreBase, MetaProfileApplicationItem, MetaProfileBookItem, MetaProfileGameItem, MetaProfileMovieItem, MetaProfileSerieItem, MetaProfileTrackItem


class ProfileService:
    @staticmethod
    def get_profiles(connected_user_uuid, page):
        """" Get user's profile list """
        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        profiles, total_pages = Paginator.get_from(
            ProfileModel.query.filter_by(user_id=user.user_id),
            page,
        )

        try:
            profile_data = ProfileBase.loads(profiles)

            return pagination_resp(
                message="Profile data sent",
                content=profile_data,
                page=page,
                total_pages=total_pages
            )

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

            profile_data = ProfileBase.load(new_profile)

            resp = message(True, "Profile created")
            resp["profile"] = profile_data

            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_data(uuid, connected_profile_uuid):
        """ Get profile's data by uuid """

        if not (user := UserModel.query.filter_by(uuid=connected_profile_uuid).first()):
            return err_resp("User not found!", 404)

        if not (profile := ProfileModel.query.filter_by(uuid=uuid).first()):
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
    def get_profile_meta_app(profile_uuid, connected_user_uuid, page):
        """ Get profile meta applicaiton """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, ApplicationModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(ApplicationModel, ApplicationModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].application = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileApplicationItem.loads(metas)

            return pagination_resp(
                message="Profile's meta application data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta_book(profile_uuid, connected_user_uuid, page):
        """ Get profile meta book """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, BookModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(BookModel, BookModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].book = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileBookItem.loads(metas)

            return pagination_resp(
                message="Profile's meta book data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta_game(profile_uuid, connected_user_uuid, page):
        """ Get profile meta game """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, GameModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(GameModel, GameModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].game = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileGameItem.loads(metas)

            return pagination_resp(
                message="Profile's meta game data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta_movie(profile_uuid, connected_user_uuid, page):
        """ Get profile meta movie """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, MovieModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(MovieModel, MovieModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].movie = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileMovieItem.loads(metas)

            return pagination_resp(
                message="Profile's meta movie data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta_serie(profile_uuid, connected_user_uuid, page):
        """ Get profile meta serie """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, SerieModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(SerieModel, SerieModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].serie = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileSerieItem.loads(metas)

            return pagination_resp(
                message="Profile's meta serie data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def get_profile_meta_track(profile_uuid, connected_user_uuid, page):
        """ Get profile meta track """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        metas, total_pages = Paginator.get_from(
            db.session.query(MetaProfileContentModel, TrackModel)
            .join(ContentModel, MetaProfileContentModel.content_id == ContentModel.content_id)
            .join(TrackModel, TrackModel.content_id == ContentModel.content_id)
            .filter(MetaProfileContentModel.profile_id == profile.profile_id),
            page,
        )

        try:
            def c_load(row):
                row[0].track = row[1]
                return row[0]

            metas = list(map(c_load, metas))
            meta_data = MetaProfileTrackItem.loads(metas)

            return pagination_resp(
                message="Profile's meta track data sent",
                content=meta_data,
                page=page,
                total_pages=total_pages
            )

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def update_meta(profile_uuid, content_id, connected_user_uuid, data):
        """ Update metadata between a profile and a content """

        if not (user := UserModel.query.filter_by(uuid=connected_user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (app := ContentModel.query.filter_by(content_id=content_id).first()):
            return err_resp("Content not found!", 404)

        # Check permissions
        permissions = get_jwt_claims()['permissions']
        if "access_sandbox" not in permissions:
            return err_resp("Permission missing", 403)

        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=user.user_id).first()):
            return err_resp("Profile not found!", 404)

        try:
            if not (meta_profile_content := MetaProfileContentModel.query.filter_by(profile_id=profile.profile_id, content_id=content_id).first()):
                meta_profile_content = MetaUserContentModel(
                    content_id=content_id, profile_id=profile.profile_id)

            meta_profile_content.rating = data["rating"]
            meta_profile_content.last_rating_date = data["last_rating_date"]
            meta_profile_content.review_see_count = data["review_see_count"]
            meta_profile_content.last_review_see_date = data["last_review_see_date"]
            meta_profile_content.count = data["count"]
            meta_profile_content.last_count_increment = data["last_count_increment"]

            db.session.add(meta_profile_content)
            db.session.commit()

            resp = message(True, "Meta successfully updated")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def launch_recommendation(profile_uuid, current_user):
        if not (profile := ProfileModel.query.filter_by(uuid=profile_uuid, user_id=current_user.user_id).first()):
            return err_resp("Profile not found!", 404)

        try:
            # Send request to reco_engine
            # TODO change url to launch for profile
            requests.put('%s/recommend/%s' % (ENGINE_URL, current_user.uuid),
                         headers={'X-API-TOKEN': ENGINE_APIKEY})

            # TODO create event for history

            resp = message(True, "Recommendation successfully started")
            return resp, 201

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
