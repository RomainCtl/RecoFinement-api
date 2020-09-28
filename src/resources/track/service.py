from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model import Track


class TrackService:
    @staticmethod
    def get_track_data(gid):
        """ Get track data by gid """
        if not (user := Track.query.filter_by(gid=gid).first()):
            return err_resp("Track not found!", 404)

        from .utils import load_data

        try:
            track_data = load_data(user)

            resp = message(True, "Track data sent")
            resp["track"] = track_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
