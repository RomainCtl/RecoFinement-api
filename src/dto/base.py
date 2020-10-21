from flask_restx import Namespace, fields, Model

# Base objects

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

GenreBaseObj = Model("Genre base", {
    "genre_id": fields.Integer,
    "name": fields.String,
    "count": fields.Integer,
})

ApplicationBaseObj = Model("Application base", {
    "app_id": fields.Integer,
    "name": fields.String,
    "categorie": fields.Nested(GenreBaseObj),
    "rating": fields.Float,
    "reviews": fields.String,
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
    "recommendations": fields.Integer,
    "release_date": fields.String,
})

MovieBaseObj = Model("Movie base", {
    "movie_id": fields.Integer,
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

MovieGenresBaseObj = Model("MovieGenres base", {
    "movie_id": fields.Integer,
    "tag": fields.String,
    "frequency": fields.Integer,
})

SerieGenresBaseObj = Model("SerieGenres base", {
    "serie_id": fields.Integer,
    "tag": fields.String,
    "frequency": fields.Integer,
})

GameGenresBaseObj = Model("GameGenres base", {
    "game_id": fields.Integer,
    "tag": fields.String,
    "frequency": fields.Integer,
})

MetaUserApplicationBaseObj = Model("MetaUserApplication base", {
    "review": fields.String,
    "rating": fields.Integer,
    "downloaded": fields.Boolean,
})

MetaUserBookBaseObj = Model("MetaUserBook base", {
    "rating": fields.Integer,
    "purchase": fields.Boolean,
})

MetaUserGameBaseObj = Model("MetaUserGame base", {
    "rating": fields.Integer,
    "purchase": fields.Boolean,
    "hours": fields.Integer,
})

MetaUserMovieBaseObj = Model("MetaUserMovie base", {
    "rating": fields.Integer,
    "watch_count": fields.Integer,
})

MetaUserSerieBaseObj = Model("MetaUserSerie base", {
    "rating": fields.Integer,
    "num_watched_episodes": fields.Integer,
})

MetaUserTrackBaseObj = Model("MetaUserTrack base", {
    "rating": fields.Integer,
    "play_count": fields.Integer,
    "last_played_date": fields.DateTime
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
    "genres": fields.List(fields.Nested(TrackGenresBaseObj)),
})

SerieItemObj2 = Model.clone("Serie Item 2", SerieItemObj, {
    "episodes": fields.List(fields.Nested(EpisodeBaseObj)),
})

TrackItemObj = Model.clone("Track Item", TrackBaseObj, {
    "genres": fields.List(fields.Nested(TrackGenresBaseObj)),
})

MovieItemObj = Model.clone("Movie Item", TrackBaseObj, {
    "genres": fields.List(fields.Nested(TrackGenresBaseObj)),
})

GameItemObj = Model.clone("Game Item", TrackBaseObj, {
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
