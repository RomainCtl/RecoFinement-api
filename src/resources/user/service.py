from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model import User


class UserService:
    @staticmethod
    def get_track_data(uuid):
        """ Get track data by uuid """
        if not (user := User.query.filter_by(uuid=uuid).first()):
            return err_resp("User not found!", "user_404", 404)

        from .utils import load_data

        try:
            user_data = load_data(user)

            resp = message(True, "User data sent")
            resp["user"] = user_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
