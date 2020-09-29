from src import db


class MovieModel(db.Model):
    """
    Movie Model for storing movie related details
    """
    __tablename__ = "movie"

    movie_id = db.Column(db.Integer, primary_key=True,
                         autoincrement=True, index=True)
    title = db.Column(db.String(255), index=True)
    genres = db.Column(db.String(255))
    language = db.Column(db.String(255))
    actors = db.Column(db.String(255))
    year = db.Column(db.String(255))
    producers = db.Column(db.String(255))
    director = db.Column(db.String(255))
    writer = db.Column(db.String(255))
    imdbid = db.Column(db.String(255))
    tmdbid = db.Column(db.String(255))
