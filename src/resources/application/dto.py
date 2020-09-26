from flask_restx import Namespace, fields


class ApplicationDto:
    api = Namespace(
        "application", description="Application related operations.")
    application = api.model(
        "Application object",
        {
            "app_id": fields.String,
            "name": fields.String,
            "category": fields.String,
            "rating": fields.Float,
            "reviews": fields.Integer,
            "size": fields.String,
            "installs": fields.String,
            "price": fields.Float,
            "content_rating": fields.String,
            "genres": fields.String,
            "last_updated": fields.String,
            "current_version": fields.String,
            "android_version": fields.String,
        },
    )

    data_resp = api.model(
        "Application Data Response",
        {
            "status": fields.Boolean,
            "message": fields.String,
            "application": fields.Nested(application),
        },
    )
