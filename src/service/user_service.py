from flask import current_app

from src import db
from src.utils import err_resp, message, pagination_resp, internal_err_resp, Paginator
from src.model import UserModel, TrackModel, MetaUserTrackModel


class UserService:
    @staticmethod
    def search_user_data(search_term, page):
        """ Search user data by username """
        users, total_pages = Paginator.get_from(
            UserModel.query.filter(
                UserModel.username.ilike("%"+search_term+"%")),
            page,
        )

        try:
            user_data = UserService._load_datas(users)

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
            user_data = UserService._load_data(user)

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()

    @staticmethod
    def give_rate(track_id, rating, user_uuid):
        """" Give rate to a track """
        if not (user := UserModel.query.filter_by(uuid=user_uuid).first()):
            return err_resp("User not found!", 404)

        if not (track := TrackModel.query.filter_by(track_id=track_id).first()):
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

    @staticmethod
    def _load_meta_tracks(meta_user_track_db_obj_list):
        """ Load meta_user_track's data

        Parameters:
        - List of meta_user_track db object
        """
        from src.schema import MetaUserTrackBase

        meta_schema = MetaUserTrackBase(many=True)

        return meta_schema.dump(meta_user_track_db_obj_list)

    @staticmethod
    def _load_datas(user_db_obj_list):
        """ Load user's data

        Parameters:
        - List of user db object
        """
        from src.schemas import UserBase

        user_schema = UserBase(many=True)

        return user_schema.dump(user_db_obj_list)

    @staticmethod
    def _load_data(user_db_obj):
        """ Load user's data

        Parameters:
        - User db object
        """
        from src.schemas import UserObject

        user_schema = UserObject()

        return user_schema.dump(user_db_obj)
