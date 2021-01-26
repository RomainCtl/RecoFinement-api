from flask_restx import Namespace, fields, Model

# Base objects

UserBaseObj = Model("User Base", {
    "uuid": fields.String,
    "email": fields.String,
    "username": fields.String,
    "preferences_defined": fields.Boolean,
})

ExternalBaseObj = Model("External service Base", {
    "service_id":  fields.Integer,
    "service_name": fields.String,
})

GroupBaseObj = Model("Group base", {
    "group_id": fields.Integer,
    "name": fields.String,
    "owner": fields.Nested(UserBaseObj)
})

GenreBaseObj = Model("Genre base", {
    "genre_id": fields.Integer,
    "name": fields.String,
    "count": fields.Integer,
})

ApplicationBaseObj = Model("Application base", {
    "content_id": fields.Integer,
    "name": fields.String,
    "categorie": fields.Nested(GenreBaseObj),
    "rating": fields.Float,
    "rating_count": fields.String,
    "size": fields.String,
    "installs": fields.String,
    "type": fields.String,
    "price": fields.String,
    "content_rating": fields.String,
    "last_updated": fields.String,
    "current_version": fields.String,
    "android_version": fields.String,
})

BookBaseObj = Model("Book base", {
    "content_id": fields.Integer,
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
    "content_id": fields.Integer,
    "steamid": fields.Integer,
    "name": fields.String,
    "short_description": fields.String,
    "header_image": fields.String,
    "website": fields.String,
    "developers": fields.String,
    "publishers": fields.String,
    "price": fields.String,
    "recommendations": fields.Integer,
    "release_date": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
})

MovieBaseObj = Model("Movie base", {
    "content_id": fields.Integer,
    "title": fields.String,
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
    "content_id": fields.Integer,
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
    "content_id": fields.Integer,
    "imdbid": fields.String,
    "title": fields.String,
    "start_year": fields.Integer,
    "end_year": fields.Integer,
    "writers": fields.String,
    "directors": fields.String,
    "actors": fields.String,
    "rating": fields.Float,
    "rating_count": fields.Integer,
})

EpisodeBaseObj = Model("Episode base", {
    "content_id": fields.Integer,
    "imdbid": fields.String,
    "title": fields.String,
    "year": fields.Integer,
    "genres": fields.String,
    "season_number": fields.Integer,
    "episode_number": fields.Integer,
    "rating": fields.Float,
    "rating_count": fields.Integer,
})

MetaUserContentBaseObj = Model("MetaUserContent base", {
    "rating": fields.Integer,
    "last_rating_date": fields.DateTime,
    "review_see_count": fields.Integer,
    "last_review_see_date": fields.DateTime,
    "count": fields.Integer,
    "last_count_increment": fields.DateTime,
})

# Item object

UserItemObj = Model.clone("User Item", UserBaseObj, {
    "groups": fields.List(fields.Nested(GroupBaseObj)),
    "invitations": fields.List(fields.Nested(GroupBaseObj)),
    "owned_groups": fields.List(fields.Nested(GroupBaseObj)),
    "liked_genres": fields.List(fields.Nested(GenreBaseObj))
})

UserExportObj = Model.clone("User Export Item", UserItemObj, {
    "meta_user_content": fields.List(fields.Nested(MetaUserContentBaseObj)),
    "linked_services": fields.List(fields.Nested(ExternalBaseObj)),
})

GroupItemObj = Model.clone("Group Item", GroupBaseObj, {
    "members": fields.List(fields.Nested(UserBaseObj)),
    "invitations": fields.List(fields.Nested(UserBaseObj))
})

SerieItemObj = Model.clone("Serie Item", SerieBaseObj, {
    "genres": fields.List(fields.Nested(GenreBaseObj)),
})

TrackItemObj = Model.clone("Track Item", TrackBaseObj, {
    "genres": fields.List(fields.Nested(GenreBaseObj)),
})

MovieItemObj = Model.clone("Movie Item", MovieBaseObj, {
    "genres": fields.List(fields.Nested(GenreBaseObj)),
})

GameItemObj = Model.clone("Game Item", GameBaseObj, {
    "genres": fields.List(fields.Nested(GenreBaseObj)),
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

# Additional Objects

ApplicationAdditionalBaseObj = Model("Application additional base", {
    "name": fields.String,
    "size": fields.String,
    "installs": fields.String,
    "type": fields.String,
    "price": fields.String,
    "content_rating": fields.String,
    "last_updated": fields.String,
    "current_version": fields.String,
    "android_version": fields.String,
    "cover": fields.String,
    "genres": fields.List(fields.Integer),
})

BookAdditionalBaseObj = Model("Book additional base", {
    "isbn": fields.String,
    "title": fields.String,
    "author": fields.String,
    "year_of_publication": fields.Integer,
    "publisher": fields.String,
    "image_url_s": fields.String,
    "image_url_m": fields.String,
    "image_url_l": fields.String
})

GameAdditionalBaseObj = Model("Game additional base", {
    "steamid": fields.Integer,
    "name": fields.String,
    "short_description": fields.String,
    "header_image": fields.String,
    "website": fields.String,
    "developers": fields.String,
    "publishers": fields.String,
    "price": fields.String,
    "release_date": fields.String,
    "genres": fields.List(fields.Integer),
})

MovieAdditionalBaseObj = Model("Movie additional base", {
    "title": fields.String,
    "language": fields.String,
    "actors": fields.String,
    "year": fields.String,
    "producers": fields.String,
    "director": fields.String,
    "writer": fields.String,
    "imdbid": fields.String,
    "tmdbid": fields.String,
    "cover": fields.String,
    "plot_outline": fields.String,
    "genres": fields.List(fields.Integer),
})

TrackAdditionalBaseObj = Model("Track additional base", {
    "title": fields.String,
    "year": fields.Integer,
    "artist_name": fields.String,
    "release": fields.String,
    "track_mmid": fields.String,
    "recording_mbid": fields.String,
    "spotify_id": fields.Float,
    "covert_art_url": fields.String,
    "genres": fields.List(fields.Integer),
})