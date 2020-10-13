from src import db


class SMovieGenresModel(db.Model):
    """
    SMovieGenres Model for storing movie genres
    """
    __tablename__ = "s_movie_genres"

    genre = db.Column(db.String(45), primary_key=True, index=True)
    count = db.Column(db.Integer)
