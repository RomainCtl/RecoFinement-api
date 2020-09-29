from flask_restx import Namespace, fields, Model

# Base  objects

UserBaseObj = Model("User Base", {
    "uuid": fields.String,
    "email": fields.String,
    "username": fields.String,
})

GroupBaseObj = Model("Group base", {
    "group_id": fields.Integer,
    "name": fields.String,
    "owner": fields.Nested(UserBaseObj)
})

TrackBaseObj = Model("Track Base", {
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
})

# Item object

UserItemObj = Model.clone("User Item", UserBaseObj, {
    "groups": fields.List(fields.Nested(GroupBaseObj)),
    "owned_groups": fields.List(fields.Nested(GroupBaseObj))
})

GroupItemObj = Model.clone("Group Item", GroupBaseObj,  {
    "members": fields.List(fields.Nested(UserBaseObj))
})

# Common Object

messageObj = Model("Basic Response", {
    "status": fields.Boolean,
    "message": fields.String,
})

validationErrorObj = Model.clone("Validation error", messageObj, {
    "errors": fields.List(fields.String),
})

paginationObj = Model("Pagination Object", {
    "status": fields.Boolean,
    "message": fields.String,
    "content": fields.List(fields.Raw),
    "number_of_elements": fields.Integer,
    "page": fields.Integer,
    "total_pages": fields.Integer,
})
