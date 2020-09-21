from flask_restx import Namespace, fields

class ApplicationDto:
    api = Namespace("application", description="Application related operations.")
    application = api.model(
        "Application object",
        {
            "uid": fields.String,
            "app_name": fields.String,
            "category": fields.String,
            "rating": fields.Float,
            "reviews": fields.Integer,
            "installs": fields.String,
            "size": fields.String,
            "price": fields.Float,
            "content_rating": fields.String,
            "last_updated": fields.String,
            "minimum_version": fields.String,
            "latest_version": fields.String,
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
