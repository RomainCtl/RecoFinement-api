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

ApplicationBaseObj = Model("Application base", {
    "app_id": fields.Integer,
    "name": fields.String,
    "category": fields.String,
    "rating": fields.Float,
    "reviews": fields.String,
    "size": fields.String,
    "installs": fields.String,
    "type": fields.String,
    "price": fields.String,
    "content_rating": fields.String,
    "genres": fields.String,
    "last_updated": fields.String,
    "current_version": fields.String,
    "android_version": fields.String,
})

BookBaseObj = Model("Book base", {
    "isbn": fields.String,
    "title": fields.String,
    "author": fields.String,
    "year_of_publication": fields.Integer,
    "publisher": fields.String,
    "image_url_s": fields.String,
    "image_url_m": fields.String,
    "image_url_l": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
})

GameBaseObj = Model("Game base", {
    "game_id": fields.Integer,
    "steamid": fields.Integer,
    "name": fields.String,
    "short_description": fields.String,
    "header_image": fields.String,
    "website": fields.String,
    "developers": fields.String,
    "publishers": fields.String,
    "price": fields.String,
    "genres": fields.String,
    "recommendations": fields.Integer,
    "release_date": fields.String,
})

MovieBaseObj = Model("Movie base", {
    "movie_id": fields.Integer,
    "title": fields.String,
    "genres": fields.String,
    "language": fields.String,
    "actors": fields.String,
    "year": fields.String,
    "producers": fields.String,
    "director": fields.String,
    "writer": fields.String,
    "imdbid": fields.String,
    "tmdbid": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
    "cover": fields.String,
})

TrackBaseObj = Model("Track base", {
    "track_id": fields.Integer,
    "title": fields.String,
    "year": fields.Integer,
    "artist_name": fields.String,
    "release": fields.String,
    "track_mmid": fields.String,
    "recording_mbid": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
    "url": fields.String,
    "covert_art_url": fields.String,
})

SerieBaseObj = Model("Serie base", {
    "serie_id": fields.Integer,
    "imdbid": fields.String,
    "title": fields.String,
    "start_year": fields.Integer,
    "end_year": fields.Integer,
    "genres": fields.String,
    "writers": fields.String,
    "directors": fields.String,
    "actors": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
})

EpisodeBaseObj = Model("Episode base", {
    "episode_id": fields.Integer,
    "imdbid": fields.String,
    "title": fields.String,
    "year": fields.Integer,
    "genres": fields.String,
    "season_number": fields.Integer,
    "episode_number": fields.Integer,
    "rating": fields.Float,
    "rating_count": fields.Integer,
    "serie": fields.Nested(SerieBaseObj),
})

TrackGenresBaseObj = Model("TrackGenres base", {
    "track_id": fields.Integer,
    "tag": fields.String,
    "frequency": fields.Integer,
})

# Item object

UserItemObj = Model.clone("User Item", UserBaseObj, {
    "groups": fields.List(fields.Nested(GroupBaseObj)),
    "invitations": fields.List(fields.Nested(GroupBaseObj)),
    "owned_groups": fields.List(fields.Nested(GroupBaseObj))
})

GroupItemObj = Model.clone("Group Item", GroupBaseObj, {
    "members": fields.List(fields.Nested(UserBaseObj)),
    "invitations": fields.List(fields.Nested(UserBaseObj))
})

SerieItemObj = Model.clone("Serie Item", SerieBaseObj, {
    "episodes": fields.List(fields.Nested(EpisodeBaseObj)),
})

TrackItemObj = Model.clone("Track Item", TrackBaseObj, {
    "genres": fields.List(fields.Nested(TrackGenresBaseObj)),
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
