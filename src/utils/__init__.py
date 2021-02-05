from .dto_schema import DTOSchema
from .sqlalchemy_auto_schema import SQLAlchemyAutoSchema
from .paginator import Paginator
from .mailjet import sendForget, sendReset, sendNewAccount
from .spotify import Spotify
from .tmdb import TMDB
from .gbooks import GBooks
from .guid import GUID
from .ws_auth import ws_jwt_required


def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object


def pagination_resp(message, content, page, total_pages):
    response_object = {
        "status": True,
        "message": message,
        "content": content,
        "number_of_elements": len(content),
        "page": page,
        "total_pages": total_pages
    }
    return response_object, 200


def validation_error(status, errors):
    if type(errors) != list:
        errors = [errors]
    response_object = {"status": status,
                       "message": "Validation errors", "errors": errors}

    return response_object, 400


def err_resp(msg, code):
    err = message(False, msg)
    return err, code


def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    return err, 500
