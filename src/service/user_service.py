from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model import UserModel


class UserService:
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
        from src.schemas import UserBase

        user_schema = UserBase()

        return user_schema.dump(user_db_obj)
