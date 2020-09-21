from flask import current_app

from src.utils import err_resp, message, internal_err_resp
from src.model.application import Application


class ApplicationService:
    @staticmethod
    def get_application_data(uid):
        """ Get application data by uid """
        if not (application := Application.query.filter_by(uid=uid).first()):
            return err_resp("Application not found!", "application_404", 404)

        from .utils import load_data

        try:
            application_data = load_data(application)

            resp = message(True, "Application data sent")
            resp["application"] = application_data
            return resp, 200

        except Exception as error:
            current_app.logger.error(error)
            return internal_err_resp()
