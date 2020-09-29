from flask_restx import Namespace, fields

UserBaseObj = {
    "uuid": fields.String,
    "email": fields.String,
    "username": fields.String,
}

TrackBaseObj = {
    "track_id": fields.String,
    "title": fields.String,
    "year": fields.Integer,
    "artist_name": fields.String,
    "release": fields.String,
    "track_mmid": fields.String,
    "recording_mbid": fields.String,
    "language": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
    "url": fields.String,
    "covert_art_url": fields.String,
}

messageObj = {
    "status": fields.Boolean,
    "message": fields.String,
}

validationErrorObj = {
    **messageObj,
    "errors": fields.List(fields.String)
}

paginationObj = {
    "status": fields.Boolean,
    "message": fields.String,
    "content": fields.List(fields.Raw),
    "number_of_elements": fields.Integer,
    "page": fields.Integer,
    "total_pages": fields.Integer
}
