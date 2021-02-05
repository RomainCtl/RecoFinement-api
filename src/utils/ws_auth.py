from flask_jwt_extended import decode_token
from flask_socketio import ConnectionRefusedError


def ws_jwt_required(f):
    @wraps
    def decorated(message):
        try:
            token = decode_token(reset_token)
        except Exception as e:
            raise ConnectionRefusedError("Unauthorized!")

        # Check identity
        if not (user := UserModel.query.filter_by(uuid=token['identity']).first()):
            raise ConnectionRefusedError("User not found!")

        # Check permissions
        # NOTE ws only used in sandbox, that's why we check this permission here
        if "access_sandbox" not in token['permissions']:
            raise ConnectionRefusedError("Permission missing!")

        return f(message, user)

    return decorated
