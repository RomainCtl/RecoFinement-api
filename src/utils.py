def message(status, message):
    response_object = {"status": status, "message": message}
    return response_object


def validation_error(status, errors):
    if type(errors) != list:
        errors = [errors]
    response_object = {"status": status, "errors": errors}

    return response_object, 400


def err_resp(msg, code):
    err = message(False, msg)
    return err, code


def internal_err_resp():
    err = message(False, "Something went wrong during the process!")
    err["error_reason"] = "server_error"
    return err, 500
