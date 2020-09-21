from flask_restx import Namespace, fields

class UserDto:
    api = Namespace("user", description="User related operations.")
    track = api.model(
        "User object",
        {
            "uuid": fields.String,
            "email": fields.String,
            "username": fields.String,
        },
    )

    data_resp = api.model(
        "User Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "user": fields.Nested(track),
        },
    )
